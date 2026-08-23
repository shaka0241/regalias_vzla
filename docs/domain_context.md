# Contexto de Negocio: Regalías Petroleras (Venezuela)

Esta librería automatiza cálculos fiscales basados en la industria de hidrocarburos de Venezuela.

## Glosario del Dominio
* **Volumen Bruto ($V_{bruto}$):** Total de fluido extraído del pozo/campo, medido en barriles (bbls). Incluye agua, arena y petróleo real.
* **BS&W (Basic Sediment and Water):** Porcentaje de impurezas en el fluido extraído, expresado en decimal (0 a 1).
* **Volumen Neto ($V_{neto}$):** Volumen de petróleo real fiscalizable.
  * *Fórmula:* $V_{neto} = V_{bruto} \times (1 - \text{BS\&W})$
* **Gravedad API:** Medida universal de densidad del petróleo.
  * **Extrapesado (< 10 API):** Crudos de la Faja Petrolífera del Orinoco. Requieren mejoramiento (diluentes) y suelen tener penalizaciones en el precio marcador.
  * **Pesado / Mediano / Liviano (> 10 API):** Crudos convencionales.
* **Precio Marcador:** Precio de referencia internacional usado para el cálculo fiscal (ej. Cesta Merey 16, Brent), expresado en USD.
* **Regalía:** Impuesto directo sobre el derecho de extracción que las operadoras pagan al Estado.

## Orden de Operaciones Matemáticas
El Motor de Regalías garantiza este orden de cálculo inalterable:
1. **Deducción de impurezas:** Cálculo de Volumen Neto.
2. **Ajuste de Precio Comercial:** Aplicación del Factor de Ajuste API sobre el precio marcador.
3. **Valoración Base:** Cálculo del Ingreso Bruto ($V_{neto} \times \text{Precio Ajustado}$).
4. **Liquidación:** Aplicación de la tasa de regalía sobre el Ingreso Bruto.

## Marco Normativo y Advertencias

- Las tasas legales provienen de la **Ley Orgánica de Hidrocarburos**
  (Decreto N° 1.510, G.O. N° 37.323 del 13/11/2001; Reforma Parcial,
  G.O. N° 38.493 del 04/08/2006): ordinaria 20 % (art. 42), banda secundaria
  hasta 30 % (art. 43) y reducción a 10 % para extrapesados de la Faja.
- El **Factor de Ajuste API es comercialmente referencial** (primas/descuentos
  por gravedad observados en el mercado): NO proviene de ningún artículo legal.
  La fórmula fiscal oficial del Ministerio incluye un ajuste por gravedad (AGA)
  cuyos valores no son públicos.
- Los cálculos son estimaciones referenciales **sin validez oficial** ante
  PDVSA, el Ministerio de Petróleo ni el SENIAT. Verifique siempre el
  instrumento vigente en la Gaceta Oficial.