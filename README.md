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

## ⚠️ Aviso legal

**`regalias_vzla` es una herramienta informática de carácter educativo y de
referencia técnica. No constituye asesoría legal, fiscal ni financiera.**

- Esta librería **no está afiliada, avalada ni patrocinada** por Petróleos de
  Venezuela, S.A. (PDVSA), el Ministerio del Poder Popular de Petróleo, el
  Servicio Nacional Integrado de Administración Aduanera y Tributaria (SENIAT)
  ni ningún otro ente del Estado venezolano.
- Los resultados son **estimaciones referenciales** basadas en tasas y factores
  configurables. **No tienen validez oficial** para declaraciones fiscales,
  liquidaciones ante PDVSA, fiscalizaciones del Ministerio de Petróleo,
  procedimientos administrativos ni procesos judiciales.
- Las tasas incorporadas reflejan el texto de la **Ley Orgánica de
  Hidrocarburos** (Decreto N° 1.510, G.O. N° 37.323 del 13/11/2001; Reforma
  Parcial, G.O. N° 38.493 del 04/08/2006) y decretos complementarios citados en
  cada módulo, pero pueden ser modificados por normas posteriores o por cambios
  en la práctica administrativa. **Verifique siempre el instrumento vigente en
  la Gaceta Oficial de la República Bolivariana de Venezuela.**
- Los factores de ajuste por gravedad API son **comercialmente referenciales**
  y no provienen de ningún artículo legal.
- El autor no garantiza la exactitud, integridad ni actualidad de los datos
  normativos, y **no asume responsabilidad** por daños derivados de su uso,
  incluidas decisiones comerciales, fiscales o de inversión. Su empleo en
  contextos profesionales (auditorías, valoraciones, litigios) exige validación
  independiente por profesionales calificados en derecho petrolero venezolano.

Licencia MIT — ver [LICENSE](LICENSE).

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

