"""Pruebas de la capa legal: tasas de regalía y factores de ajuste API."""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from regalias_vzla.marco_legal import (
    FACTOR_AJUSTE_LIVIANO,
    TASA_REGALIA_ESTANDAR,
    TASA_REGALIA_EXTRAPESADO,
    TASA_REGALIA_SECUNDARIA,
    BandaAjusteApi,
    TablaAjusteApi,
    TasaLegal,
    factor_ajuste_api,
)


class TestFactorAjusteApi:
    @pytest.mark.parametrize(
        ("gravedad_api", "factor_esperado"),
        [
            (8.5, "0.90"),
            (9.99, "0.90"),
            (10.0, "0.95"),
            (15.0, "0.95"),
            (21.99, "0.95"),
            (22.0, "1.00"),
            (29.9, "1.00"),
            (30.0, "1.05"),
            (45.0, "1.05"),
        ],
    )
    def test_bandas_de_la_tabla(self, gravedad_api: float, factor_esperado: str) -> None:
        assert factor_ajuste_api(gravedad_api) == Decimal(factor_esperado)

    def test_factor_liviano_expuesto(self) -> None:
        factor = FACTOR_AJUSTE_LIVIANO
        assert factor == Decimal("1.05")


class TestTasaLegal:
    def test_extrapesado_tributa_diez_por_ciento(self) -> None:
        tasa = TasaLegal.para_gravedad_api(8.5)
        assert tasa.tasa_regalia == TASA_REGALIA_EXTRAPESADO == Decimal("0.10")
        assert "extrapesado" in tasa.nombre.lower()

    def test_convencional_tributa_veinte_por_ciento(self) -> None:
        tasa = TasaLegal.para_gravedad_api(25)
        assert tasa.tasa_regalia == TASA_REGALIA_ESTANDAR == Decimal("0.20")

    def test_frontera_diez_grados_es_convencional(self) -> None:
        assert TasaLegal.para_gravedad_api(10).tasa_regalia == TASA_REGALIA_ESTANDAR

    def test_tasa_personalizada_valida(self) -> None:
        tasa = TasaLegal(tasa_regalia="0.15")
        assert tasa.tasa_regalia == Decimal("0.15")

    @pytest.mark.parametrize("tasa_invalida", ["0", "1.5", "-0.2"])
    def test_tasas_fuera_de_rango_lanzan_error(self, tasa_invalida: str) -> None:
        with pytest.raises(ValidationError):
            TasaLegal(tasa_regalia=tasa_invalida)

    def test_modelo_congelado(self) -> None:
        tasa = TasaLegal.para_gravedad_api(25)
        with pytest.raises(ValidationError):
            tasa.tasa_regalia = Decimal("0.50")  # type: ignore[misc]


class TestTablaAjusteApi:
    def test_tabla_oficial_reproduce_los_factores(self) -> None:
        tabla = TablaAjusteApi.oficial()
        assert tabla.factor_para(8.5) == Decimal("0.90")
        assert tabla.factor_para(15.0) == Decimal("0.95")
        assert tabla.factor_para(25.0) == Decimal("1.00")
        assert tabla.factor_para(35.0) == Decimal("1.05")

    def test_tabla_personalizada_sin_banda_superior(self) -> None:
        tabla = TablaAjusteApi(
            bandas=(BandaAjusteApi(hasta_gravedad=100, factor="1.00"),),
            factor_final="1.00",
        )
        assert tabla.factor_para(8.5) == Decimal("1.00")
        assert tabla.factor_para(45.0) == Decimal("1.00")

    def test_factor_final_personalizado(self) -> None:
        tabla = TablaAjusteApi(
            bandas=(BandaAjusteApi(hasta_gravedad=20, factor="0.80"),),
            factor_final="1.50",
        )
        assert tabla.factor_para(19.9) == Decimal("0.80")
        assert tabla.factor_para(20.0) == Decimal("1.50")

    @pytest.mark.parametrize(
        "bandas",
        [
            (
                BandaAjusteApi(hasta_gravedad=30, factor="0.90"),
                BandaAjusteApi(hasta_gravedad=20, factor="0.95"),
            ),
            (
                BandaAjusteApi(hasta_gravedad=20, factor="0.90"),
                BandaAjusteApi(hasta_gravedad=20, factor="0.95"),
            ),
        ],
    )
    def test_limites_no_ascendentes_lanzan_validation_error(
        self, bandas: tuple[BandaAjusteApi, ...]
    ) -> None:
        with pytest.raises(ValidationError):
            TablaAjusteApi(bandas=bandas)

    def test_factor_fuera_de_rango_lanza_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            BandaAjusteApi(hasta_gravedad=20, factor="3")

    def test_tabla_vacia_lanza_validation_error(self) -> None:
        with pytest.raises(ValidationError):
            TablaAjusteApi(bandas=())

    def test_modelo_congelado(self) -> None:
        tabla = TablaAjusteApi.oficial()
        with pytest.raises(ValidationError):
            tabla.factor_final = Decimal("2")  # type: ignore[misc]


class TestTasaSecundaria:
    def test_secundaria_treinta_por_ciento(self) -> None:
        tasa = TasaLegal.secundaria()
        assert tasa.tasa_regalia == TASA_REGALIA_SECUNDARIA == Decimal("0.30")
