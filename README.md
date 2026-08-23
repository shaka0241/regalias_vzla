# regalias_vzla

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
