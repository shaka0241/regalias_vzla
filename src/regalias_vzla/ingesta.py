"""Capa de adaptadores: ingesta segura de datos externos hacia el dominio."""

from __future__ import annotations

import csv
import io
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from regalias_vzla.fluidos import FluidoCrudo

_ALIAS_COLUMNAS: dict[str, str] = {
    "volumenbruto": "volumen_bruto",
    "volbruto": "volumen_bruto",
    "volumen": "volumen_bruto",
    "bbls": "volumen_bruto",
    "bsw": "bs_w",
    "bswpercent": "bs_w",
    "basicsedimentwater": "bs_w",
    "sedimentosyaguas": "bs_w",
    "gravedadapi": "gravedad_api",
    "api": "gravedad_api",
}

_CAMPOS_REQUERIDOS = frozenset({"volumen_bruto", "bs_w", "gravedad_api"})


def _normalizar_encabezado(encabezado: str) -> str:
    return "".join(caracter for caracter in encabezado.lower() if caracter.isalnum())


def _mapear_registro(fila: Mapping[str, Any], origen: str) -> dict[str, Any]:
    mapeado: dict[str, Any] = {}
    for clave, valor in fila.items():
        canonico = _ALIAS_COLUMNAS.get(_normalizar_encabezado(str(clave)))
        if canonico is not None:
            mapeado[canonico] = valor
    faltantes = _CAMPOS_REQUERIDOS.difference(mapeado)
    if faltantes:
        raise ValueError(
            f"{origen}: columnas requeridas ausentes o desconocidas: {sorted(faltantes)}"
        )
    return mapeado


def parsear_registros(registros: Iterable[Mapping[str, Any]]) -> list[FluidoCrudo]:
    """Valida una secuencia de diccionarios crudos contra el dominio.

    Acepta claves canónicas (``volumen_bruto``) o alias habituales
    (``bbls``, ``BSW``, ``api``). Los registros inválidos lanzan
    ``pydantic.ValidationError``.
    """
    return [
        FluidoCrudo.model_validate(_mapear_registro(registro, f"registro {numero}"))
        for numero, registro in enumerate(registros, start=1)
    ]


def parsear_csv(contenido: str | bytes) -> list[FluidoCrudo]:
    """Parsea el contenido textual de un CSV hacia modelos del dominio."""
    if isinstance(contenido, bytes):
        contenido = contenido.decode("utf-8-sig")
    lector = csv.DictReader(io.StringIO(contenido))
    if lector.fieldnames is None:
        raise ValueError("CSV vacío: se requiere al menos la fila de encabezados.")
    filas = list(lector)
    return [
        FluidoCrudo.model_validate(_mapear_registro(fila, f"fila {numero}"))
        for numero, fila in enumerate(filas, start=2)
    ]


def cargar_csv(ruta: str | Path) -> list[FluidoCrudo]:
    """Lee un archivo CSV desde disco y lo parsea de forma segura."""
    try:
        contenido = Path(ruta).read_bytes().decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ValueError(f"No se pudo decodificar '{ruta}' como UTF-8: {error}") from error
    return parsear_csv(contenido)


def parsear_json(contenido: str | bytes) -> list[FluidoCrudo]:
    """Parsea JSON (lista de registros u objeto con clave 'registros')."""
    datos = json.loads(contenido)
    if isinstance(datos, Mapping) and "registros" in datos:
        datos = datos["registros"]
    if not isinstance(datos, list):
        raise ValueError(
            "El JSON debe ser una lista de registros o un objeto con clave 'registros'."
        )
    return parsear_registros(datos)


def cargar_json(ruta: str | Path) -> list[FluidoCrudo]:
    """Lee un archivo JSON desde disco y lo parsea de forma segura."""
    try:
        contenido = Path(ruta).read_bytes()
    except OSError as error:
        raise ValueError(f"No se pudo leer el archivo '{ruta}': {error}") from error
    try:
        return parsear_json(contenido)
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON inválido en '{ruta}': {error}") from error
