# regalias_vzla

[![CI](https://github.com/shaka0241/regalias_vzla/actions/workflows/ci.yml/badge.svg)](https://github.com/shaka0241/regalias_vzla/actions/workflows/ci.yml)

Librería Python para el cálculo automatizado de **regalías petroleras venezolanas**, con validación estricta de tipos (Pydantic), modelos inmutables y un orden matemático de liquidación garantizado.

## Instalación (desarrollo)

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -e .[dev]
```

Requiere Python 3.9 o superior.

## Uso rápido

```python
from decimal import Decimal

from regalias_vzla import FluidoCrudo, MotorRegalias, TasaLegal

fluido = FluidoCrudo(volumen_bruto="100000", bs_w="0.02", gravedad_api=8.5)
motor = MotorRegalias(TasaLegal.para_gravedad_api(fluido.gravedad_api))
resultado = motor.liquidar(fluido, precio_marcador=Decimal("70"))

print(resultado.regalia_usd)  # Decimal('617400.00')
print(resultado.model_dump_json())  # serializable a APIs / archivos
```

Orden de cálculo inalterable:

1. Deducción de impurezas → volumen neto.
2. Ajuste del precio marcador por factor API.
3. Ingreso bruto = volumen neto × precio ajustado.
4. Regalía = ingreso bruto × tasa legal.

## Estructura

| Módulo          | Responsabilidad                                        |
| --------------- | ------------------------------------------------------ |
| `fluidos.py`    | Capa física: validación y volúmenes netos              |
| `marco_legal.py`| Tasas impositivas y factores de ajuste API             |
| `calculo.py`    | Orquestador financiero (`MotorRegalias`)               |
| `ingesta.py`    | Adaptadores CSV / JSON hacia los modelos de dominio    |

Ver `docs/` para contexto de dominio, arquitectura y guía de contribución.

## Desarrollo

```bash
pytest            # tests
ruff check .      # lint
mypy              # chequeo estático estricto
```

## Publicación a PyPI

El workflow `release.yml` se dispara al crear un tag `v*`:

```bash
git tag v0.1.0 && git push origin v0.1.0
```

Pipeline: verifica que el tag coincida con la versión (`pyproject.toml` y `__init__.py`) → build sdist/wheel → `twine check` → smoke test del wheel en Python 3.9–3.13 → publicación con **Trusted Publishing** (OIDC).

Requisito único de configuración (una vez): dar de alta el *trusted publisher* en [PyPI](https://pypi.org/manage/account/publishing/) con owner `shaka0241`, repo `regalias_vzla`, workflow `release.yml`, environment `pypi`.

