"""Blindaje anti-drift: los ejemplos de examples/ deben producir su salida documentada.

Cada script de examples/ se ejecuta como subproceso y su stdout se compara
contra una salida esperada exacta. Si un cambio en la librería altera un
resultado, este test falla y obliga a actualizar ejemplo y documentación a la vez.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
EJEMPLOS = RAIZ / "examples"

SALIDAS_ESPERADAS: dict[str, str] = {
    "01_calculo_basico.py": """\
Fluido: 100000 bbl brutos, BS&W 0.02, 8.5 °API
Volumen neto fiscalizable: 98000.000000 bbl
Precio marcador: 70.00 USD/bbl
Factor API aplicado: 0.90
Precio ajustado: 63.00 USD/bbl
Ingreso bruto: 6174000.00 USD
Tasa aplicada: Regalía extrapesado (Faja Petrolífera) - 10 % (0.10)
Regalía a pagar: 617400.00 USD
""",
    "02_tasa_secundaria.py": """\
Volumen neto: 49750.000000 bbl
Ingreso bruto: 3980000.00 USD
Ordinaria 20 %: 796000.00 USD
Secundaria 30 %: 1194000.00 USD
Costo adicional de la banda secundaria: 398000.00 USD
""",
    "03_tabla_api_personalizada.py": """\
Tabla oficial → factor 0.90, regalía 617400.00 USD
Tabla neutra → factor 1.00, regalía 686000.00 USD
Impacto de eliminar la penalización extrapesado: 68600.00 USD
""",
    "04_ingesta_csv_json.py": """\
Liquidación por fila del CSV:
    8.5 °API → regalía 617400.00 USD
   25.0 °API → regalía 696500.00 USD
Total CSV: 1313900.00 USD
JSON con alias: 31.0 °API → regalía 1164240.00 USD
""",
    "05_manejo_errores.py": """\
Validación física (1 error): bs_w: less_than_equal
Precio '-5' rechazado:
El precio marcador debe ser un número finito mayor que cero; recibido: Decimal('-5')
Precio '0' rechazado:
El precio marcador debe ser un número finito mayor que cero; recibido: Decimal('0')
CSV incompleto: fila 2: columnas requeridas ausentes o desconocidas: ['bs_w', 'gravedad_api']
""",
    "06_serializacion_api.py": (
        '{"volumen_neto_bbl":98000.0,"precio_marcador_usd":70.0,'
        '"factor_ajuste_api":0.9,"precio_ajustado_usd":63.0,'
        '"ingreso_bruto_usd":6174000.0,"tasa_aplicada":0.1,"regalia_usd":617400.0}\n'
        "Round-trip fiel: True\n"
        "ResultadoRegalia es inmutable: no admite mutaciones\n"
    ),
}


@pytest.mark.parametrize(("nombre", "salida_esperada"), sorted(SALIDAS_ESPERADAS.items()), ids=str)
def test_ejemplo_produce_salida_documentada(nombre: str, salida_esperada: str) -> None:
    proceso = subprocess.run(
        [sys.executable, str(EJEMPLOS / nombre)],
        capture_output=True,
        text=True,
        check=False,
        cwd=RAIZ,
    )
    assert proceso.returncode == 0, proceso.stderr
    assert proceso.stdout == salida_esperada
