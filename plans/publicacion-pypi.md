# Plan: Pendientes para publicar `regalias_vzla` en PyPI

Estado de la auditoría previa a la primera publicación (tag `v0.1.0`).

## Hecho

- [x] Crear `LICENSE` (MIT) en la raíz.
- [x] Añadir «Aviso legal» al README y disclaimer corto en `__init__.py`.
- [x] Corregir citas legales: «Ley **Orgánica** de Hidrocarburos», G.O. N° 37.323 del 13/11/2001, Reforma Parcial G.O. N° 38.493 del 04/08/2006 (pyproject, README, docs, marco_legal.py).
- [x] Docstring normativo en `marco_legal.py` con citas por constante (art. 42 → 20 %, art. 43 + Decreto 5.330 → 30 %, Decreto 4.889 → 10 %).
- [x] Rotular `TablaAjusteApi.oficial()` como referencial comercial, no statutory.
- [x] `pyproject.toml`: `setuptools>=77`, `license-files`, `[project.urls]`, classifier Python 3.13, descripción corregida.
- [x] Crear `CHANGELOG.md`; rellenar `docs/README.md`.
- [x] Verificación local: ruff ✓, mypy strict ✓, 76 tests ✓, `python -m build` + `twine check` ✓.

## Pendiente (bloqueantes antes del primer tag)

- [ ] Dar de alta el *trusted publisher* en <https://pypi.org/manage/account/publishing/>:
      owner `shaka0241` · repo `regalias_vzla` · workflow `release.yml` · environment `pypi`.
      Debe existir **antes** del primer push del tag (la primera publicación va por OIDC).

## Pendiente (recomendados)

- [ ] Verificar en Gaceta Oficial el **Decreto N° 4.889** (regalía reducida 10 %,
      extrapesados Faja; citado como G.O. N° 37.458 del 24/06/2002 — marcado
      *[Verificar]* en docstrings y docs) antes de usarlo en producción.
- [ ] Opcional: `CITATION.cff`, badge de licencia en README.

## Checklist de release

```bash
git tag v0.1.0 && git push origin v0.1.0
```

Pipeline (`release.yml`): verifica tag ↔ versión (`pyproject.toml` y `__init__.py`)
→ build sdist/wheel → `twine check` → smoke test Python 3.9–3.13 → publicación
vía Trusted Publishing.

Nota: en PyPI el nombre normalizado es `regalias-vzla` (disponible, verificado
contra la API de PyPI).
