"""Ejemplo 2: tasa de banda secundaria (30 %) para campos de alta productividad.

Compara la liquidación de un mismo crudo bajo la tasa ordinaria (20 %,
art. 42 LOH) y la tasa secundaria (30 %, art. 43 LOH).

Ejecutar: python examples/02_tasa_secundaria.py
"""

from decimal import Decimal

from regalias_vzla import FluidoCrudo, MotorRegalias, TasaLegal

fluido = FluidoCrudo(volumen_bruto="50000", bs_w="0.005", gravedad_api=25)
precio = Decimal("80")

ordinario = MotorRegalias(TasaLegal.para_gravedad_api(fluido.gravedad_api))
secundario = MotorRegalias(TasaLegal.secundaria())

resultado_ordinario = ordinario.liquidar(fluido, precio_marcador=precio)
resultado_secundario = secundario.liquidar(fluido, precio_marcador=precio)

print(f"Volumen neto: {resultado_ordinario.volumen_neto_bbl} bbl")
print(f"Ingreso bruto: {resultado_ordinario.ingreso_bruto_usd} USD")
print(f"Ordinaria 20 %: {resultado_ordinario.regalia_usd} USD")
print(f"Secundaria 30 %: {resultado_secundario.regalia_usd} USD")

diferencia = resultado_secundario.regalia_usd - resultado_ordinario.regalia_usd
print(f"Costo adicional de la banda secundaria: {diferencia} USD")
