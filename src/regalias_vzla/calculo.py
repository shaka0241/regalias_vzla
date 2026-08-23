"""Orquestador financiero: motor de liquidación de regalías."""

from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal, localcontext

from pydantic import BaseModel, ConfigDict, Field, field_serializer

from regalias_vzla.fluidos import FluidoCrudo
from regalias_vzla.marco_legal import TablaAjusteApi, TasaLegal

_CENTIMO = Decimal("0.01")
_MILLESIMA_BBL = Decimal("0.000001")
_PRECISION_INTERNA = 40


def _a_decimal(valor: Decimal | float | int | str) -> Decimal:
    return valor if isinstance(valor, Decimal) else Decimal(str(valor))


class ResultadoRegalia(BaseModel):
    """Liquidación inmutable y serializable de una regalía petrolera."""

    model_config = ConfigDict(frozen=True)

    volumen_neto_bbl: Decimal = Field(description="Volumen neto fiscalizable en barriles.")
    precio_marcador_usd: Decimal = Field(description="Precio de referencia en USD/bbl.")
    factor_ajuste_api: Decimal = Field(description="Factor comercial aplicado por densidad API.")
    precio_ajustado_usd: Decimal = Field(description="Precio marcador ajustado por API (USD/bbl).")
    ingreso_bruto_usd: Decimal = Field(description="Volumen neto x precio ajustado (USD).")
    tasa_aplicada: Decimal = Field(description="Tasa de regalía aplicada, en decimal.")
    regalia_usd: Decimal = Field(description="Regalía a pagar al Estado (USD).")

    @field_serializer(
        "volumen_neto_bbl",
        "precio_marcador_usd",
        "factor_ajuste_api",
        "precio_ajustado_usd",
        "ingreso_bruto_usd",
        "tasa_aplicada",
        "regalia_usd",
    )
    def _serializar_decimal(self, valor: Decimal) -> float:
        return float(valor)


class MotorRegalias:
    """Ejecuta el orden matemático inalterable de liquidación fiscal.

    Orden garantizado:

    1. Deducción de impurezas (volumen neto).
    2. Ajuste del precio marcador por factor API.
    3. Valoración base (ingreso bruto).
    4. Liquidación (regalía según tasa legal).
    """

    def __init__(
        self, tasa_legal: TasaLegal, tabla_ajuste_api: TablaAjusteApi | None = None
    ) -> None:
        self._tasa_legal = tasa_legal
        self._tabla_ajuste_api = (
            tabla_ajuste_api if tabla_ajuste_api is not None else TablaAjusteApi.oficial()
        )

    @property
    def tasa_legal(self) -> TasaLegal:
        """Tasa legal inyectada a este motor."""
        return self._tasa_legal

    @property
    def tabla_ajuste_api(self) -> TablaAjusteApi:
        """Tabla de factores de ajuste API usada por este motor."""
        return self._tabla_ajuste_api

    def liquidar(
        self,
        fluido: FluidoCrudo,
        precio_marcador: Decimal | float | int | str,
    ) -> ResultadoRegalia:
        """Liquida la regalía de un fluido al precio marcador indicado.

        Lanza ``ValueError`` si el precio es inconsistente con el negocio
        (negativo, cero o no finito). Los montos monetarios se redondean a
        centavos (ROUND_HALF_UP); el volumen, a seis decimales.
        """
        precio = _a_decimal(precio_marcador)
        if not precio.is_finite() or precio <= 0:
            raise ValueError(
                "El precio marcador debe ser un número finito mayor que cero; "
                f"recibido: {precio_marcador!r}"
            )

        with localcontext() as contexto:
            contexto.prec = _PRECISION_INTERNA
            factor = self._tabla_ajuste_api.factor_para(fluido.gravedad_api)
            volumen_neto = fluido.volumen_neto
            precio_ajustado = precio * factor
            ingreso_bruto = volumen_neto * precio_ajustado
            regalia = ingreso_bruto * self._tasa_legal.tasa_regalia

        return ResultadoRegalia(
            volumen_neto_bbl=volumen_neto.quantize(_MILLESIMA_BBL, rounding=ROUND_HALF_UP),
            precio_marcador_usd=precio.quantize(_CENTIMO, rounding=ROUND_HALF_UP),
            factor_ajuste_api=factor,
            precio_ajustado_usd=precio_ajustado.quantize(_CENTIMO, rounding=ROUND_HALF_UP),
            ingreso_bruto_usd=ingreso_bruto.quantize(_CENTIMO, rounding=ROUND_HALF_UP),
            tasa_aplicada=self._tasa_legal.tasa_regalia,
            regalia_usd=regalia.quantize(_CENTIMO, rounding=ROUND_HALF_UP),
        )
