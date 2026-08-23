"""Capa física: definición y validación del dominio de fluidos."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

GRAVEDAD_EXTRAPESADO = 10.0


class FluidoCrudo(BaseModel):
    """Parámetros físicos del fluido extraído de un pozo o campo.

    El volumen bruto incluye agua y sedimentos; el volumen neto fiscalizable
    se obtiene deduciendo el BS&W:

        V_neto = V_bruto x (1 - BS&W)
    """

    model_config = ConfigDict(frozen=True)

    volumen_bruto: Decimal = Field(
        ...,
        gt=0,
        description="Volumen bruto extraído en barriles (incluye agua y arena).",
    )
    bs_w: Decimal = Field(
        ...,
        ge=0,
        le=1,
        description="Basic Sediment & Water, en decimal (0 a 1).",
    )
    gravedad_api: float = Field(
        ...,
        gt=0,
        description="Densidad del crudo en grados API (< 10 es extrapesado).",
    )

    @property
    def es_extrapesado(self) -> bool:
        """Indica si el crudo pertenece a la banda extrapesada (< 10° API)."""
        return self.gravedad_api < GRAVEDAD_EXTRAPESADO

    @property
    def volumen_neto(self) -> Decimal:
        """Volumen de petróleo real fiscalizable, tras deducir impurezas."""
        return self.volumen_bruto * (Decimal("1") - self.bs_w)
