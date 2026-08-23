"""regalias_vzla: cálculo automatizado de regalías petroleras venezolanas.

Herramienta de carácter educativo y de referencia técnica. NO constituye
asesoría legal, fiscal ni financiera; no está afiliada ni avalada por PDVSA,
el Ministerio de Petróleo, el SENIAT ni ningún ente del Estado venezolano.
Los resultados son estimaciones referenciales SIN validez oficial. Verifique
siempre el instrumento vigente en la Gaceta Oficial. Licencia MIT.
"""

from regalias_vzla.calculo import MotorRegalias, ResultadoRegalia
from regalias_vzla.fluidos import GRAVEDAD_EXTRAPESADO, FluidoCrudo
from regalias_vzla.ingesta import (
    cargar_csv,
    cargar_json,
    parsear_csv,
    parsear_json,
    parsear_registros,
)
from regalias_vzla.marco_legal import (
    TASA_REGALIA_ESTANDAR,
    TASA_REGALIA_EXTRAPESADO,
    TASA_REGALIA_SECUNDARIA,
    BandaAjusteApi,
    TablaAjusteApi,
    TasaLegal,
)
from regalias_vzla.marco_legal import factor_ajuste_api as factor_ajuste_api

__version__ = "0.1.0"

__all__ = [
    "GRAVEDAD_EXTRAPESADO",
    "TASA_REGALIA_ESTANDAR",
    "TASA_REGALIA_EXTRAPESADO",
    "TASA_REGALIA_SECUNDARIA",
    "BandaAjusteApi",
    "FluidoCrudo",
    "MotorRegalias",
    "ResultadoRegalia",
    "TablaAjusteApi",
    "TasaLegal",
    "__version__",
    "cargar_csv",
    "cargar_json",
    "factor_ajuste_api",
    "parsear_csv",
    "parsear_json",
    "parsear_registros",
]
