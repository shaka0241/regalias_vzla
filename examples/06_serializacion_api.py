"""Ejemplo 6: serialización JSON y round-trip del resultado.

``ResultadoRegalia`` es serializable a JSON numérico (ideal para APIs y
archivos), restaurable con ``model_validate_json`` e inmutable.

Ejecutar: python examples/06_serializacion_api.py
"""

from decimal import Decimal

from pydantic import ValidationError

from regalias_vzla import FluidoCrudo, MotorRegalias, ResultadoRegalia, TasaLegal

fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
resultado = MotorRegalias(TasaLegal.para_gravedad_api(8.5)).liquidar(
    fluido, precio_marcador=Decimal("70")
)

texto_json = resultado.model_dump_json()
print(texto_json)

restaurado = ResultadoRegalia.model_validate_json(texto_json)
print(f"Round-trip fiel: {restaurado == resultado}")

try:
    resultado.regalia_usd = Decimal("1")
except ValidationError:
    print("ResultadoRegalia es inmutable: no admite mutaciones")
