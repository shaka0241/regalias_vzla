"""Pruebas de los adaptadores de ingesta CSV / JSON."""

import json
from decimal import Decimal

import pytest
from pydantic import ValidationError

from regalias_vzla.ingesta import (
    cargar_csv,
    cargar_json,
    parsear_csv,
    parsear_json,
    parsear_registros,
)

CSV_VALIDO = """Volumen Bruto,BsW,API
100000,0.02,8.5
50000,0.005,25
"""

CSV_CON_ALIAS_CANONICO = """volumen_bruto,bs_w,gravedad_api
1000,0.1,30
"""

JSON_LISTA = [
    {"volumen_bruto": "100000", "bs_w": "0.02", "gravedad_api": 8.5},
]

JSON_ENVUELTO = {"registros": JSON_LISTA}


class TestParsearCsv:
    def test_encabezados_comerciales_con_alias(self) -> None:
        fluidos = parsear_csv(CSV_VALIDO)
        assert len(fluidos) == 2
        assert fluidos[0].volumen_neto == Decimal("98000")
        assert fluidos[1].gravedad_api == 25

    def test_claves_canonicas_tambien_son_aceptadas(self) -> None:
        fluidos = parsear_csv(CSV_CON_ALIAS_CANONICO)
        assert len(fluidos) == 1
        assert fluidos[0].bs_w == Decimal("0.1")

    def test_fila_fisicamente_invalida_lanza_validation_error(self) -> None:
        contenido = "volumen_bruto,bs_w,gravedad_api\n1000,1.5,30\n"
        with pytest.raises(ValidationError):
            parsear_csv(contenido)

    def test_columnas_ausentes_lanzan_value_error(self) -> None:
        with pytest.raises(ValueError, match="columnas requeridas"):
            parsear_csv("volumen_bruto\n1000\n")

    def test_csv_vacio_lanza_value_error(self) -> None:
        with pytest.raises(ValueError, match="vacío"):
            parsear_csv("")


class TestParsearJson:
    def test_lista_de_registros(self) -> None:
        fluidos = parsear_json(json.dumps(JSON_LISTA))
        assert len(fluidos) == 1
        assert fluidos[0].es_extrapesado is True

    def test_objeto_con_clave_registros(self) -> None:
        fluidos = parsear_json(json.dumps(JSON_ENVUELTO))
        assert len(fluidos) == 1

    def test_forma_invalida_lanza_value_error(self) -> None:
        with pytest.raises(ValueError):
            parsear_json('{"no_es_una_lista": true}')

    def test_registro_invalido_lanza_validation_error(self) -> None:
        registro = [{"volumen_bruto": "-1", "bs_w": "0", "gravedad_api": 30}]
        with pytest.raises(ValidationError):
            parsear_json(json.dumps(registro))


class TestParsearRegistros:
    def test_diccionarios_canonicos(self) -> None:
        registros = [{"volumen_bruto": 50000, "bs_w": 0.005, "gravedad_api": 25}]
        fluidos = parsear_registros(registros)
        assert fluidos[0].volumen_neto == Decimal("49750")


class TestCargaDesdeArchivo:
    def test_cargar_csv_y_json_desde_ruta(self, tmp_path) -> None:
        ruta_csv = tmp_path / "produccion.csv"
        ruta_csv.write_text(CSV_VALIDO, encoding="utf-8")
        assert len(cargar_csv(ruta_csv)) == 2

        ruta_json = tmp_path / "produccion.json"
        ruta_json.write_text(json.dumps(JSON_ENVUELTO), encoding="utf-8")
        assert len(cargar_json(ruta_json)) == 1
