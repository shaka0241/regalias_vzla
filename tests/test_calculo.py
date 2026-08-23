"""Pruebas del orquestador financiero: MotorRegalias y ResultadoRegalia."""

from __future__ import annotations

from decimal import Decimal

import pytest
from pydantic import ValidationError

from regalias_vzla import FluidoCrudo, MotorRegalias, ResultadoRegalia, TasaLegal


@pytest.fixture
def motor_extrapesado() -> MotorRegalias:
    return MotorRegalias(TasaLegal.para_gravedad_api(8.5))


class TestLiquidacion:
    def test_caso_extrapesado_valores_exactos(
        self, fluido_extrapesado: FluidoCrudo, motor_extrapesado: MotorRegalias
    ) -> None:
        resultado = motor_extrapesado.liquidar(fluido_extrapesado, precio_marcador="70")

        assert resultado.volumen_neto_bbl == Decimal("98000")
        assert resultado.precio_marcador_usd == Decimal("70.00")
        assert resultado.factor_ajuste_api == Decimal("0.90")
        assert resultado.precio_ajustado_usd == Decimal("63.00")
        assert resultado.ingreso_bruto_usd == Decimal("6174000.00")
        assert resultado.tasa_aplicada == Decimal("0.10")
        assert resultado.regalia_usd == Decimal("617400.00")

    def test_caso_convencional_sin_ajuste(self, fluido_mediano: FluidoCrudo) -> None:
        motor = MotorRegalias(TasaLegal.para_gravedad_api(25))
        resultado = motor.liquidar(fluido_mediano, precio_marcador=80)

        assert resultado.volumen_neto_bbl == Decimal("49750")
        assert resultado.precio_ajustado_usd == Decimal("80.00")
        assert resultado.ingreso_bruto_usd == Decimal("3980000.00")
        assert resultado.regalia_usd == Decimal("796000.00")

    def test_acepta_varios_tipos_de_precio(self, fluido_mediano: FluidoCrudo) -> None:
        motor = MotorRegalias(TasaLegal.para_gravedad_api(25))
        esperado = Decimal("796000.00")
        assert motor.liquidar(fluido_mediano, 80).regalia_usd == esperado
        assert motor.liquidar(fluido_mediano, "80").regalia_usd == esperado
        assert motor.liquidar(fluido_mediano, Decimal("80")).regalia_usd == esperado

    def test_orden_de_operaciones_respeta_formula(
        self, fluido_extrapesado: FluidoCrudo, motor_extrapesado: MotorRegalias
    ) -> None:
        resultado = motor_extrapesado.liquidar(fluido_extrapesado, precio_marcador=70)

        ingreso_recalculado = fluido_extrapesado.volumen_neto * resultado.precio_ajustado_usd
        regalia_recalculada = ingreso_recalculado * resultado.tasa_aplicada
        assert resultado.ingreso_bruto_usd == ingreso_recalculado.quantize(Decimal("0.01"))
        assert resultado.regalia_usd == regalia_recalculada.quantize(Decimal("0.01"))

    def test_tasa_legal_accesible_desde_motor(self, motor_extrapesado: MotorRegalias) -> None:
        assert motor_extrapesado.tasa_legal.tasa_regalia == Decimal("0.10")


class TestInconsistenciasDeNegocio:
    @pytest.mark.parametrize("precio_invalido", ["-5", "0", "-0.01", float("nan"), float("inf")])
    def test_precio_invalido_lanza_value_error(
        self,
        fluido_mediano: FluidoCrudo,
        precio_invalido: str | float,
    ) -> None:
        motor = MotorRegalias(TasaLegal.para_gravedad_api(25))
        with pytest.raises(ValueError):
            motor.liquidar(fluido_mediano, precio_invalido)


class TestResultadoRegalia:
    def test_modelo_congelado(
        self, fluido_extrapesado: FluidoCrudo, motor_extrapesado: MotorRegalias
    ) -> None:
        resultado = motor_extrapesado.liquidar(fluido_extrapesado, precio_marcador=70)
        with pytest.raises(ValidationError):
            resultado.regalia_usd = Decimal("1")  # type: ignore[misc]

    def test_serializacion_json_numerica(
        self, fluido_extrapesado: FluidoCrudo, motor_extrapesado: MotorRegalias
    ) -> None:
        resultado = motor_extrapesado.liquidar(fluido_extrapesado, precio_marcador=70)
        json_texto = resultado.model_dump_json()
        assert '"regalia_usd":617400.0' in json_texto
        restaurado = ResultadoRegalia.model_validate_json(json_texto)
        assert restaurado == resultado
