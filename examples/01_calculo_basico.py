"""Ejemplo 1: cálculo básico de una regalía con el flujo completo.

Pasos del flujo: definir la física del pozo, seleccionar la tasa legal
según la banda API y liquidar al precio marcador indicado.

Ejecutar: python examples/01_calculo_basico.py
"""

from decimal import Decimal

from regalias_vzla import FluidoCrudo, MotorRegalias, TasaLegal

fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
tasa = TasaLegal.para_gravedad_api(fluido.gravedad_api)

motor = MotorRegalias(tasa)
resultado = motor.liquidar(fluido, precio_marcador=Decimal("70"))

print(f"Fluido: {fluido.volumen_bruto} bbl brutos, BS&W {fluido.bs_w}, {fluido.gravedad_api} °API")
print(f"Volumen neto fiscalizable: {resultado.volumen_neto_bbl} bbl")
print(f"Precio marcador: {resultado.precio_marcador_usd} USD/bbl")
print(f"Factor API aplicado: {resultado.factor_ajuste_api}")
print(f"Precio ajustado: {resultado.precio_ajustado_usd} USD/bbl")
print(f"Ingreso bruto: {resultado.ingreso_bruto_usd} USD")
print(f"Tasa aplicada: {tasa.nombre} ({resultado.tasa_aplicada})")
print(f"Regalía a pagar: {resultado.regalia_usd} USD")
