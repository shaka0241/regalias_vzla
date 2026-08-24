# Contribuir a regalias_vzla

¡Gracias por tu interés en contribuir a este proyecto Open Source! Para mantener la integridad de los cálculos fiscales, seguimos un proceso estricto de desarrollo.

## Entorno de Desarrollo Local

1. Haz un fork del repositorio y clónalo localmente.
2. Crea un entorno virtual e instala las dependencias de desarrollo:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -e .[dev]
   ```
3. Verifica que el entorno está listo:
   ```bash
   pytest -q
   ```

## Calidad obligatoria antes de cada PR

La CI (`.github/workflows/ci.yml`) ejecuta exactamente estas comprobaciones;
tu PR debe pasarlas en local antes de abrirse:

```bash
pytest --cov=regalias_vzla --cov-report=term-missing   # suite completa con cobertura
ruff check .                                            # lint
ruff format --check .                                   # formato canónico
mypy                                                    # chequeo estático estricto (src/)
```

- La suite corre en Python **3.9–3.13**: no uses sintaxis posterior a 3.9.
- `mypy` es estricto y solo aplica a `src/`, pero todo código nuevo debe
  estar anotado igualmente.

## Convenciones del proyecto

- **Español** para docstrings, nombres, mensajes de error y documentación.
- **`Decimal`** para todo valor monetario o volumétrico; nunca `float` en
  cálculos fiscales.
- Modelos Pydantic **inmutables** (`frozen=True`): ni `FluidoCrudo`,
  `TasaLegal`, `TablaAjusteApi` ni `ResultadoRegalia` admiten mutación.
- El **orden matemático de liquidación es inalterable** (deducción de
  impurezas → ajuste API → ingreso bruto → regalía). Cualquier cambio en ese
  orden requiere discusión previa en un issue.
- Toda constante normativa en `marco_legal.py` cita su instrumento legal
  (artículo LOH, número de decreto y Gaceta Oficial) en el docstring del
  módulo o en el comentario adyacente.
- Los factores de `TablaAjusteApi.oficial()` son referenciales; cualquier
  modificación debe mantener la advertencia de que no son statutory.

## Galería de ejemplos (`examples/`)

Cada script de `examples/` se ejecuta como subproceso en la suite
(`tests/test_ejemplos.py`) y su salida se compara contra una salida esperada
exacta. Si tu cambio altera resultados:

1. Ejecuta el ejemplo afectado: `python examples/01_calculo_basico.py`.
2. Verifica que el nuevo resultado sea correcto.
3. Actualiza la salida esperada en `tests/test_ejemplos.py` y cualquier
   valor citado en `README.md` o `docs/`.

Así ningún ejemplo documentado puede quedar desactualizado respecto al código.

## Estructura de módulos

| Módulo           | Responsabilidad                                  |
| ---------------- | ------------------------------------------------ |
| `fluidos.py`     | Validación física y volumen neto                 |
| `marco_legal.py` | Tasas legales y factores de ajuste API           |
| `calculo.py`     | Motor de liquidación y resultado serializable    |
| `ingesta.py`     | Adaptadores CSV / JSON hacia los modelos         |

## Proceso para contribuir

1. Abre un issue describiendo el cambio (o comenta en uno existente).
2. Crea una rama descriptiva desde `main`: `git checkout -b feat/mi-cambio`.
3. Realiza cambios atómicos con mensajes claros.
4. Añade o ajusta tests: toda funcionalidad nueva llega con pruebas, y todo
   bug corregido llega con el test que lo reproduce.
5. Ejecuta las cuatro comprobaciones de la sección anterior hasta verde.
6. Actualiza [`CHANGELOG.md`](../CHANGELOG.md) bajo "No publicado".
7. Abre el Pull Request describiendo qué cambia y por qué.

## Cambios normativos

Si modificas tasas, umbrales o fórmulas legales:

- Cita el instrumento vigente (artículo, decreto y **Gaceta Oficial** con
  fecha) en el docstring correspondiente.
- Actualiza [`domain_context.md`](domain_context.md) y el aviso del
  [`README.md`](../README.md) si aplica.
- Marca como `[Verificar]` toda referencia no confirmada en Gaceta, como se
  hace hoy con el Decreto N° 4.889.
