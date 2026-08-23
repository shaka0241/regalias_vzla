"""Capa de negocio gubernamental: tasas legales y ajustes de precio por API."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from regalias_vzla.fluidos import GRAVEDAD_EXTRAPESADO

TASA_REGALIA_EXTRAPESADO = Decimal("0.10")
TASA_REGALIA_ESTANDAR = Decimal("0.20")
TASA_REGALIA_SECUNDARIA = Decimal("0.30")

FACTOR_AJUSTE_NEUTRO = Decimal("1.00")
FACTOR_AJUSTE_LIVIANO = Decimal("1.05")


class BandaAjusteApi(BaseModel):
    """Banda de densidad API con su factor comercial asociado."""

    model_config = ConfigDict(frozen=True)

    hasta_gravedad: float = Field(
        ...,
        gt=0,
        description="Límite superior exclusivo de la banda, en grados API.",
    )
    factor: Decimal = Field(
        ...,
        gt=0,
        le=2,
        description="Multiplicador aplicado al precio marcador.",
    )


class TablaAjusteApi(BaseModel):
    """Tabla ordenada y configurable de factores de ajuste API.

    El factor se resuelve con la primera banda cuyo límite superior sea
    mayor que la gravedad del crudo; para gravedades iguales o superiores
    al último límite se aplica ``factor_final``.
    """

    model_config = ConfigDict(frozen=True)

    bandas: tuple[BandaAjusteApi, ...] = Field(min_length=1)
    factor_final: Decimal = Field(
        default=FACTOR_AJUSTE_NEUTRO,
        gt=0,
        le=2,
        description="Factor aplicado por encima del último límite de banda.",
    )

    @field_validator("bandas")
    @classmethod
    def _limites_estricamente_ascendentes(
        cls, bandas: tuple[BandaAjusteApi, ...]
    ) -> tuple[BandaAjusteApi, ...]:
        limites = [banda.hasta_gravedad for banda in bandas]
        if any(actual >= siguiente for actual, siguiente in zip(limites, limites[1:])):
            raise ValueError(
                "Los límites de las bandas deben estar ordenados de forma estrictamente ascendente."
            )
        return bandas

    def factor_para(self, gravedad_api: float) -> Decimal:
        """Factor aplicable a un crudo con la gravedad API indicada."""
        for banda in self.bandas:
            if gravedad_api < banda.hasta_gravedad:
                return banda.factor
        return self.factor_final

    @classmethod
    def oficial(cls) -> TablaAjusteApi:
        """Tabla referencial venezolana (punto de partida configurable).

        - < 10° API    → ``0.90`` (penalización extrapesado / diluentes)
        - 10° a 21.99° → ``0.95`` (crudo pesado)
        - 22° a 29.99° → ``1.00`` (crudo mediano, neutro)
        - >= 30°       → ``1.05`` (prima crudo liviano)
        """
        return cls(
            bandas=(
                BandaAjusteApi(hasta_gravedad=GRAVEDAD_EXTRAPESADO, factor=Decimal("0.90")),
                BandaAjusteApi(hasta_gravedad=22.0, factor=Decimal("0.95")),
                BandaAjusteApi(hasta_gravedad=30.0, factor=FACTOR_AJUSTE_NEUTRO),
            ),
            factor_final=FACTOR_AJUSTE_LIVIANO,
        )


def factor_ajuste_api(gravedad_api: float) -> Decimal:
    """Atajo de ``TablaAjusteApi.oficial().factor_para(gravedad_api)``."""
    return TablaAjusteApi.oficial().factor_para(gravedad_api)


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

    @classmethod
    def secundaria(cls) -> TasaLegal:
        """Tasa de banda secundaria: campos de alta productividad al 30 %."""
        return cls(
            nombre="Regalía de banda secundaria - 30 %",
            tasa_regalia=TASA_REGALIA_SECUNDARIA,
        )
