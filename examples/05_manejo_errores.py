"""Ejemplo 5: manejo de errores del dominio y de la ingesta.

Tres familias de fallo: validación física (``ValidationError`` de
Pydantic), inconsistencias de negocio en el precio (``ValueError``) y
columnas CSV ausentes o desconocidas (``ValueError``).

Ejecutar: python examples/05_manejo_errores.py
"""

from decimal import Decimal

from pydantic import ValidationError

from regalias_vzla import FluidoCrudo, MotorRegalias, TasaLegal, parsear_csv

try:
    FluidoCrudo(volumen_bruto="1000", bs_w="1.5", gravedad_api=30)
except ValidationError as error:
    detalles = ", ".join(f"{e['loc'][0]}: {e['type']}" for e in error.errors(include_url=False))
    print(f"Validación física ({error.error_count()} error): {detalles}")

fluido_valido = FluidoCrudo(volumen_bruto="50000", bs_w="0.005", gravedad_api=25)
motor = MotorRegalias(TasaLegal.secundaria())

for precio_invalido in ("-5", "0"):
    try:
        motor.liquidar(fluido_valido, precio_marcador=Decimal(precio_invalido))
    except ValueError as error:
        print(f"Precio '{precio_invalido}' rechazado:")
        print(error)

try:
    parsear_csv("volumen_bruto\n1000\n")
except ValueError as error:
    print(f"CSV incompleto: {error}")
