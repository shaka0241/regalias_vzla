"""Fixtures compartidos para la suite de pruebas."""

from decimal import Decimal

import pytest

from regalias_vzla import FluidoCrudo


@pytest.fixture
def fluido_extrapesado() -> FluidoCrudo:
    return FluidoCrudo(volumen_bruto=Decimal("100000"), bs_w=Decimal("0.02"), gravedad_api=8.5)


@pytest.fixture
def fluido_mediano() -> FluidoCrudo:
    return FluidoCrudo(volumen_bruto=Decimal("50000"), bs_w=Decimal("0.005"), gravedad_api=25)
