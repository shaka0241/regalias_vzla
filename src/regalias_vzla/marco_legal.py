"""Capa de negocio gubernamental: tasas legales y ajustes de precio por API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from regalias_vzla.fluidos import GRAVEDAD_EXTRAPESADO

TASA_REGALIA_ESTANDAR = Decimal("0.20")
TASA_REGALIA_EXTRAPESADO = Decimal("0.10")

FACTOR_AJUSTE_NEUTRO = Decimal("1.00")
FACTOR_AJUSTE_LIVIANO = Decimal("1.05")

_TABLA_FACTORES_API: tuple[tuple[float, Decimal], ...] = (
    (GRAVEDAD_EXTRAPESADO, Decimal("0.90")),
    (22.0, Decimal("0.95")),
    (30.0, FACTOR_AJUSTE_NEUTRO),
)


def factor_ajuste_api(gravedad_api: float) -> Decimal:
    """Factor comercial que ajusta el precio marcador según densidad API.

    Tabla referencial:

    - < 10° API    → ``0.90`` (penalización extrapesado / diluentes)
    - 10° a 21.99° → ``0.95`` (crudo pesado)
    - 22° a 29.99° → ``1.00`` (crudo mediano, neutro)
    - >= 30°       → ``1.05`` (prima crudo liviano)
    """
    for limite_superior, factor in _TABLA_FACTORES_API:
        if gravedad_api < limite_superior:
            return factor
    return FACTOR_AJUSTE_LIVIANO


class TasaLegal(BaseModel):
    """Tasa de regalía vigente inyectada al motor de cálculo."""

    model_config = ConfigDict(frozen=True)

    nombre: str = Field(default="Regalía ordinaria - Ley de Hidrocarburos")
    tasa_regalia: Decimal = Field(..., gt=0, le=1, description="Tasa en decimal (0.20 = 20 %).")

    @classmethod
    def para_gravedad_api(cls, gravedad_api: float) -> TasaLegal:
        """Selecciona la tasa según la banda API del crudo.

        Crudos extrapesados (< 10° API) tributan al 10 %; el resto, al 20 %.
        """
        if gravedad_api < GRAVEDAD_EXTRAPESADO:
            return cls(
                nombre="Regalía extrapesado (Faja Petrolífera) - 10 %",
                tasa_regalia=TASA_REGALIA_EXTRAPESADO,
            )
        return cls(nombre="Regalía ordinaria - 20 %", tasa_regalia=TASA_REGALIA_ESTANDAR)
