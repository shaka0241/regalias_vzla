"""Pruebas de la capa física: validación y volúmenes netos."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from regalias_vzla.fluidos import GRAVEDAD_EXTRAPESADO, FluidoCrudo


class TestValidacion:
    def test_crea_fluido_valido(self) -> None:
        fluido = FluidoCrudo(
            volumen_bruto=Decimal("100000"),
            bs_w=Decimal("0.02"),
            gravedad_api=8.5,
        )
        assert fluido.volumen_bruto == Decimal("100000")
        assert fluido.bs_w == Decimal("0.02")
        assert fluido.gravedad_api == 8.5

    def test_coercion_de_cadenas(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api="8.5")
        assert fluido.volumen_bruto == Decimal("100000")
        assert fluido.bs_w == Decimal("0.02")
        assert fluido.gravedad_api == 8.5

    def test_bs_w_en_cero_es_valido(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="1000", bs_w="0", gravedad_api=30)
        assert fluido.bs_w == Decimal("0")

    def test_bs_w_en_uno_es_valido(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="1000", bs_w="1", gravedad_api=30)
        assert fluido.volumen_neto == Decimal("0")

    @pytest.mark.parametrize(
        ("campo", "valor"),
        [
            ("volumen_bruto", "0"),
            ("volumen_bruto", "-10"),
            ("bs_w", "-0.01"),
            ("bs_w", "1.01"),
            ("gravedad_api", "0"),
            ("gravedad_api", "-15"),
            ("gravedad_api", float("inf")),
            ("gravedad_api", float("-inf")),
            ("gravedad_api", float("nan")),
            ("gravedad_api", "80.1"),
        ],
    )
    def test_valores_invalidos_lanzan_validation_error(self, campo: str, valor: str) -> None:
        datos = {"volumen_bruto": "1000", "bs_w": "0.1", "gravedad_api": "25"}
        datos[campo] = valor
        with pytest.raises(ValidationError):
            FluidoCrudo.model_validate(datos)

    def test_gravedad_api_en_cota_superior_es_valido(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="1000", bs_w="0.1", gravedad_api=80)
        assert fluido.gravedad_api == 80


class TestCalculos:
    def test_formula_volumen_neto(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
        assert fluido.volumen_neto == Decimal("98000")

    def test_volumen_neto_sin_impurezas_iguala_bruto(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="7777", bs_w="0", gravedad_api=22)
        assert fluido.volumen_neto == Decimal("7777")


class TestClasificacionApi:
    def test_crudo_extrapesado(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="1000", bs_w="0", gravedad_api=GRAVEDAD_EXTRAPESADO - 2)
        assert fluido.es_extrapesado is True

    def test_crudo_convencional_en_frontera(self) -> None:
        fluido = FluidoCrudo(volumen_bruto="1000", bs_w="0", gravedad_api=GRAVEDAD_EXTRAPESADO)
        assert fluido.es_extrapesado is False


class TestInmutabilidad:
    def test_modelo_congelado(self, fluido_mediano: FluidoCrudo) -> None:
        with pytest.raises(ValidationError):
            fluido_mediano.volumen_bruto = Decimal("999")  # type: ignore[misc]
