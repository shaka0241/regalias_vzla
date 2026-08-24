"""Ejemplo 3: tabla de ajuste API personalizada.

La tabla oficial es referencial y configurable: se puede inyectar una
propia al motor sin tocar el orden matemático de la liquidación.

Ejecutar: python examples/03_tabla_api_personalizada.py
"""

from decimal import Decimal

from regalias_vzla import (
    BandaAjusteApi,
    FluidoCrudo,
    MotorRegalias,
    TablaAjusteApi,
    TasaLegal,
)

fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
tasa = TasaLegal.para_gravedad_api(fluido.gravedad_api)
precio = Decimal("70")

tabla_oficial = TablaAjusteApi.oficial()
tabla_neutra = TablaAjusteApi(
    bandas=(BandaAjusteApi(hasta_gravedad=100, factor=Decimal("1.00")),),
    factor_final=Decimal("1.00"),
)

con_oficial = MotorRegalias(tasa, tabla_ajuste_api=tabla_oficial).liquidar(
    fluido, precio_marcador=precio
)
con_neutra = MotorRegalias(tasa, tabla_ajuste_api=tabla_neutra).liquidar(
    fluido, precio_marcador=precio
)

print(
    f"Tabla oficial → factor {con_oficial.factor_ajuste_api}, regalía {con_oficial.regalia_usd} USD"
)
print(f"Tabla neutra → factor {con_neutra.factor_ajuste_api}, regalía {con_neutra.regalia_usd} USD")

impacto = con_neutra.regalia_usd - con_oficial.regalia_usd
print(f"Impacto de eliminar la penalización extrapesado: {impacto} USD")
