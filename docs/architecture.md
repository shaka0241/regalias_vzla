# Arquitectura del Proyecto: regalias_vzla

## Principios de Diseño
El proyecto sigue un enfoque de **Domain-Driven Design (DDD)** adaptado a una librería de cálculo funcional. Priorizamos la **Developer Experience (DX)** y la seguridad (Type Safety) utilizando Pydantic para garantizar que cálculos fiscales por millones de dólares no fallen por errores de tipos de datos.

## Estructura de Módulos (`src/regalias_vzla/`)

* **`fluidos.py` (Capa Física):** Define el dominio físico. 
  * **Responsabilidad:** Validar parámetros físicos (ej. BS&W no mayor a 1) y calcular volúmenes netos.
* **`marco_legal.py` (Capa de Negocio Gubernamental):** Define el entorno regulatorio. 
  * **Responsabilidad:** Almacenar tasas impositivas y lógica de primas/penalizaciones (Factores de Ajuste API).
* **`calculo.py` (Orquestador Financiero):** El motor principal.
  * **Responsabilidad:** Cruzar volúmenes netos con precios marcadores y tasas para emitir objetos `ResultadoRegalia` inmutables.
* **`ingesta.py` (Capa de Adaptadores):** Interfaces para sistemas externos.
  * **Responsabilidad:** Ingerir datos crudos (CSV, JSON) y parsearlos de forma segura hacia los modelos de dominio.

## Flujo de Datos (Data Flow)
1. **Validación:** Los datos crudos entran por `ingesta.py` o instanciación directa. `Pydantic` valida rangos y tipos.
2. **Contexto:** Se inyecta la instancia de `TasaLegal` aplicable.
3. **Cálculo:** `MotorRegalias` ejecuta operaciones en un orden matemático estricto.
4. **Salida:** Retorna un modelo inmutable que puede ser consumido por APIs o convertido a JSON/CSV.

## Manejo de Errores
- Invalidez de formato físico/financiero: Lanza `pydantic.ValidationError`.
- Inconsistencia de negocio (ej. precio negativo): Lanza `ValueError`.