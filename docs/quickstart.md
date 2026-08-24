# Guía Rápida (Quickstart): regalias_vzla

> **Aviso legal:** herramienta educativa y de referencia técnico. No constituye
> asesoría legal, fiscal ni financiera; los resultados no tienen validez oficial
> ante PDVSA, el Ministerio de Petróleo ni el SENIAT.

## Instalación

La librería está disponible en el Python Package Index (PyPI) y es compatible con Python 3.9 o superior. En PyPI el nombre normalizado es `regalias-vzla`.

```bash
pip install regalias-vzla
```

Para trabajar sobre una copia del repositorio:

```bash
git clone https://github.com/shaka0241/regalias_vzla
cd regalias_vzla
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -e .[dev]
```

## Primer cálculo

Tres pasos: definir la **física del pozo** (`FluidoCrudo`), seleccionar la
**tasa legal** según la banda API y liquidar con el **motor de cálculo**.

```python
from decimal import Decimal

from regalias_vzla import FluidoCrudo, MotorRegalias, TasaLegal

fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
tasa = TasaLegal.para_gravedad_api(fluido.gravedad_api)

motor = MotorRegalias(tasa)
resultado = motor.liquidar(fluido, precio_marcador=Decimal("70"))

print(resultado.regalia_usd)  # Decimal('617400.00')
```

Qué acaba de pasar (el orden matemático es inalterable):

1. Deducción de impurezas → `100000 × (1 − 0.02)` = **98 000 bbl netos**.
2. Ajuste del precio marcador por factor API → crudo extrapesado (< 10 °API)
   recibe factor `0.90`: `70 × 0.90` = **63.00 USD/bbl**.
3. Ingreso bruto = `98000 × 63.00` = **6 174 000 USD**.
4. Regalía = `6174000 × 0.10` (tasa extrapesado, Decreto N° 4.889) =
   **617 400 USD**.

## El resultado, campo a campo

`ResultadoRegalia` expone cada paso intermedio para auditoría:

| Campo                 | Valor en el ejemplo | Significado                                    |
| --------------------- | ------------------- | ---------------------------------------------- |
| `volumen_neto_bbl`    | `98000.000000`      | Volumen fiscalizable tras deducir BS&W         |
| `precio_marcador_usd` | `70.00`             | Precio de referencia recibido                  |
| `factor_ajuste_api`   | `0.90`              | Factor comercial aplicado por gravedad API     |
| `precio_ajustado_usd` | `63.00`             | Marcador ajustado por API                      |
| `ingreso_bruto_usd`   | `6174000.00`        | Volumen neto × precio ajustado                 |
| `tasa_aplicada`       | `0.10`              | Tasa legal usada (`0.20` ordinaria, `0.30` secundaria) |
| `regalia_usd`         | `617400.00`         | Regalía a pagar al Estado                      |

Los montos se redondean a centavos (`ROUND_HALF_UP`) y el volumen a seis
decimales. Los factores de `TablaAjusteApi.oficial()` son referenciales de
práctica comercial; puede inyectar su propia tabla al motor:

```python
from decimal import Decimal

from regalias_vzla import BandaAjusteApi, MotorRegalias, TablaAjusteApi

tabla_propia = TablaAjusteApi(
    bandas=(BandaAjusteApi(hasta_gravedad=10, factor=Decimal("0.92")),),
    factor_final=Decimal("1.00"),
)
motor = MotorRegalias(tasa, tabla_ajuste_api=tabla_propia)
```

## Errores que verá

- `pydantic.ValidationError`: parámetros físicos fuera de rango
  (`bs_w > 1`, volúmenes negativos, gravedades ≤ 0).
- `ValueError` al liquidar: precio marcador negativo, cero o no finito.
- `ValueError` en ingesta: CSV sin encabezados o columnas requeridas
  ausentes/desconocidas.

Todos los mensajes son en español e incluyen el detalle del campo fallido.

## Siguientes pasos

| Recurso                                   | Contenido                                          |
| ----------------------------------------- | -------------------------------------------------- |
| [`../examples/`](../examples/)            | Galería de scripts ejecutables y verificados en CI |
| [`domain_context.md`](domain_context.md)  | Glosario del dominio y orden de operaciones        |
| [`architecture.md`](architecture.md)      | Estructura de módulos y decisiones de diseño       |

Ejemplos disponibles: cálculo básico, tasa secundaria, tabla API personalizada,
ingesta CSV/JSON, manejo de errores y serialización JSON. Cada script imprime
su salida esperada; la suite de pruebas ejecuta todos en cada commit para
garantizar que nunca queden desactualizados.
