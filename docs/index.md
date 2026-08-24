--8<-- "docs/includes/aviso_legal.md"

# regalias_vzla

Librería Python para el cálculo automatizado de **regalías petroleras
venezolanas** conforme a la **Ley Orgánica de Hidrocarburos** (Decreto N° 1.510,
G.O. N° 37.323 del 13/11/2001; Reforma Parcial, G.O. N° 38.493 del 04/08/2006),
con validación estricta de tipos (Pydantic), modelos inmutables y un orden
matemático de liquidación garantizado.

## Instalación

```bash
pip install regalias-vzla
```

Compatible con Python 3.9 o superior.

## Uso rápido

```python
from decimal import Decimal

from regalias_vzla import FluidoCrudo, MotorRegalias, TasaLegal

fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
motor = MotorRegalias(TasaLegal.para_gravedad_api(fluido.gravedad_api))
resultado = motor.liquidar(fluido, precio_marcador=Decimal("70"))

print(resultado.regalia_usd)  # Decimal('617400.00')
```

Orden de cálculo inalterable:

1. Deducción de impurezas → volumen neto.
2. Ajuste del precio marcador por factor API.
3. Ingreso bruto = volumen neto × precio ajustado.
4. Regalía = ingreso bruto × tasa legal.

## Recorrido sugerido

| Sección | Contenido |
| --- | --- |
| [Guía rápida](quickstart.md) | Instalación, primer cálculo y lectura del resultado |
| [Contexto de dominio](domain_context.md) | Glosario petrolero y orden de operaciones |
| [Arquitectura](architecture.md) | Estructura de módulos y decisiones de diseño |
| [Referencia API](api/fluidos.md) | Firmas completas generadas desde los docstrings |
| [Ejemplos](https://github.com/shaka0241/regalias_vzla/tree/main/examples) | Scripts ejecutables verificados en CI |
| [Contribuir](contributing.md) | Convenciones y proceso de PR |

## Galería de ejemplos

| Ejemplo | Contenido |
| --- | --- |
| `01_calculo_basico.py` | Flujo completo: fluido → tasa → liquidación |
| `02_tasa_secundaria.py` | Banda secundaria 30 % vs. ordinaria 20 % |
| `03_tabla_api_personalizada.py` | Tabla de ajuste API configurable |
| `04_ingesta_csv_json.py` | CSV / JSON con alias comerciales |
| `05_manejo_errores.py` | `ValidationError` y `ValueError` del dominio |
| `06_serializacion_api.py` | JSON, round-trip e inmutabilidad |

## Referencias normativas

- Ley Orgánica de Hidrocarburos — Decreto N° 1.510 con Fuerza de Ley,
  **G.O. N° 37.323 del 13/11/2001** (arts. 42 y 43: regalía ordinaria 20 %,
  banda secundaria hasta 30 %).
- Reforma Parcial de la LOH — **G.O. N° 38.493 del 04/08/2006**.
- Decreto N° 5.330 (umbrales de productividad de la banda secundaria) —
  **G.O. N° 38.270 del 23/09/2005**.
- Decreto N° 4.889 (regalía reducida para extrapesados de la Faja, < 10 °API) —
  **G.O. N° 37.458 del 24/06/2002** *(pendiente de verificación final en
  Gaceta)*.

Los factores de ajuste por gravedad API (`TablaAjusteApi.oficial()`) son
**comercialmente referenciales** y no provienen de ningún artículo legal.
Verifique siempre el instrumento vigente en la Gaceta Oficial de la República
Bolivariana de Venezuela.
