# Documentación de `regalias_vzla`

Librería Python para el cálculo automatizado de **regalías petroleras
venezolanas** conforme a la **Ley Orgánica de Hidrocarburos** (Decreto N° 1.510,
G.O. N° 37.323 del 13/11/2001; Reforma Parcial, G.O. N° 38.493 del 04/08/2006).

> **Aviso legal:** herramienta educativa y de referencia técnico. No constituye
> asesoría legal, fiscal ni financiera, y no está afiliada ni avalada por PDVSA,
> el Ministerio de Petróleo, el SENIAT ni ningún ente del Estado venezolano.
> Los resultados son estimaciones referenciales sin validez oficial.

## Índice

| Documento | Contenido |
| --- | --- |
| [`quickstart.md`](quickstart.md) | Instalación y primer cálculo |
| [`domain_context.md`](domain_context.md) | Glosario del dominio y orden de operaciones |
| [`architecture.md`](architecture.md) | Estructura de módulos y decisiones de diseño |
| [`contributing.md`](contributing.md) | Guía para contribuir |

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
