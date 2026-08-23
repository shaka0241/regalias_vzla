"""Prueba extremo a extremo: ingesta → dominio → motor → serialización."""

import json
from decimal import Decimal

from regalias_vzla import (
    FluidoCrudo,
    MotorRegalias,
    TasaLegal,
    cargar_json,
    parsear_csv,
)

CSV_PRODUCCION = """Volumen Bruto,BsW,API
100000,0.02,8.5
50000,0.005,25
"""


def test_flujo_completo_de_ingesta_a_regalia() -> None:
    fluidos = parsear_csv(CSV_PRODUCCION)
    assert len(fluidos) == 2

    liquidaciones = []
    for fluido in fluidos:
        motor = MotorRegalias(TasaLegal.para_gravedad_api(fluido.gravedad_api))
        liquidaciones.append(motor.liquidar(fluido, precio_marcador=Decimal("70")))

    extrapesado, convencional = liquidaciones
    assert extrapesado.regalia_usd == Decimal("617400.00")
    assert convencional.regalia_usd == Decimal("696500.00")


def test_serializacion_json_del_resultado() -> None:
    fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
    resultado = MotorRegalias(TasaLegal.para_gravedad_api(8.5)).liquidar(
        fluido, precio_marcador=Decimal("70")
    )

    datos = json.loads(resultado.model_dump_json())
    assert datos["regalia_usd"] == 617400.0
    assert datos["ingreso_bruto_usd"] == 6174000.00


def test_ingesta_json_envuelto_y_liquidacion(tmp_path) -> None:
    ruta = tmp_path / "produccion.json"
    ruta.write_text(
        json.dumps([{"volumen_bruto": "100000", "bs_w": 0.02, "gravedad_api": 8.5}]),
        encoding="utf-8",
    )

    (fluido,) = cargar_json(ruta)
    resultado = MotorRegalias(TasaLegal.para_gravedad_api(fluido.gravedad_api)).liquidar(
        fluido, precio_marcador=70
    )
    assert resultado.regalia_usd == Decimal("617400.00")
