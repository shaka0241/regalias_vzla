"""Ejemplo 4: ingesta de CSV y JSON hacia el dominio.

Los adaptadores aceptan encabezados canónicos (``volumen_bruto``, ``bs_w``,
``gravedad_api``) o alias habituales (``bbls``, ``BSW``, ``api``, ...).
Para archivos en disco use ``cargar_csv(ruta)`` / ``cargar_json(ruta)``.

Ejecutar: python examples/04_ingesta_csv_json.py
"""

import json
from decimal import Decimal

from regalias_vzla import MotorRegalias, TasaLegal, parsear_csv, parsear_json

CSV_PRODUCCION = """Volumen Bruto,BsW,API
100000,0.02,8.5
50000,0.005,25
"""

JSON_PRODUCCION = json.dumps(
    {
        "registros": [
            {"volumen": "80000", "bswpercent": "0.01", "api": 31},
        ]
    }
)

print("Liquidación por fila del CSV:")
total_csv = Decimal("0")
for fluido in parsear_csv(CSV_PRODUCCION):
    motor = MotorRegalias(TasaLegal.para_gravedad_api(fluido.gravedad_api))
    resultado = motor.liquidar(fluido, precio_marcador=Decimal("70"))
    total_csv += resultado.regalia_usd
    print(f"  {fluido.gravedad_api:>5} °API → regalía {resultado.regalia_usd} USD")
print(f"Total CSV: {total_csv} USD")

(fluido_json,) = parsear_json(JSON_PRODUCCION)
motor = MotorRegalias(TasaLegal.para_gravedad_api(fluido_json.gravedad_api))
resultado = motor.liquidar(fluido_json, precio_marcador=Decimal("70"))
print(f"JSON con alias: {fluido_json.gravedad_api} °API → regalía {resultado.regalia_usd} USD")
