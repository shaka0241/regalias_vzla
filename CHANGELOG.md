# Changelog

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y [SemVer](https://semver.org/lang/es/).

## [0.1.0] - 2026-08-23
### Added
- `FluidoCrudo`: validación física (BS&W, gravedad API) y cálculo de volumen neto.
- `TasaLegal`: tasas de regalía ordinaria (20 %, art. 42 LOH), banda secundaria
  (30 %, art. 43 LOH) y extrapesado (10 %, Faja Petrolífera del Orinoco).
- `TablaAjusteApi`: factores de ajuste API configurables (tabla oficial referencial).
- `MotorRegalias`: orden de liquidación inalterable (impurezas → precio ajustado
  → ingreso bruto → regalía) con aritmética `Decimal`.
- Adaptadores CSV/JSON (`ingesta.py`) y marcador `py.typed`.
