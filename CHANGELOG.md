# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [SemVer](https://semver.org/lang/es/).

## [No publicado]
### Added
- Sitio de documentación con MkDocs Material + mkdocstrings: referencia API
  auto-generada de los 4 módulos, guías, changelog integrado y aviso legal
  como snippet reutilizable. Despliegue a GitHub Pages vía
  `.github/workflows/docs.yml` (build `--strict`). Extra `[docs]` en
  `pyproject.toml` y URL `Documentation` en los metadatos.
- Galería de ejemplos `examples/` (6 scripts ejecutables: cálculo básico, tasa
  secundaria, tabla API personalizada, ingesta CSV/JSON, manejo de errores y
  serialización JSON) con test anti-drift (`tests/test_ejemplos.py`) que
  verifica su salida en cada commit.
- Documentación completada: `docs/quickstart.md` (instalación, primer cálculo,
  lectura del resultado campo a campo) y `docs/contributing.md` (calidad,
  convenciones y proceso de PR).

## [0.1.0] - 2026-08-23
### Added
- `FluidoCrudo`: validación física (BS&W, gravedad API) y cálculo de volumen neto.
- `TasaLegal`: tasas de regalía ordinaria (20 %, art. 42 LOH), banda secundaria
  (30 %, art. 43 LOH) y extrapesado (10 %, Faja Petrolífera del Orinoco).
- `TablaAjusteApi`: factores de ajuste API configurables (tabla oficial referencial).
- `MotorRegalias`: orden de liquidación inalterable (impurezas → precio ajustado
  → ingreso bruto → regalía) con aritmética `Decimal`.
- Adaptadores CSV/JSON (`ingesta.py`) y marcador `py.typed`.
