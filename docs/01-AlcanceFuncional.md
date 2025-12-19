# Sistema RAG sobre JUS – Provincia de Córdoba

## Dominio

Exclusivo: Provincia de Córdoba.

Unidad de cálculo: JUS como unidad primaria, pesos como conversión derivada.

Normativa base:
- Código Arancelario Ley 9459 y modificatorias.
- Tabla oficial histórica y vigente del valor del JUS.

## Funcionalidades incluidas

### 1. Consultas normativas

Responder preguntas sobre:

- servicios profesionales y su valuación en JUS
- mínimos, máximos y rangos
- reglas de cálculo según tipo de proceso

Siempre con cita normativa explícita (artículo y ley).

*Ejemplos:*

“¿Cuántos JUS corresponde un divorcio bilateral?”
“¿Cuál es el mínimo de JUS para una consulta escrita?”

### 2. Valor del JUS

Obtener:

- valor vigente del JUS
- valor histórico por fecha
- variaciones entre períodos

*Ejemplos:*

“¿Cuánto vale hoy el JUS en Córdoba?”
“¿Cuál era el valor del JUS en junio de 2022?”

### 3. Conversión automática

Cálculos determinísticos:

- JUS → pesos
- pesos → JUS

Usando:

- fecha explícita indicada por el usuario

- o último valor vigente si no se indica fecha

*Ejemplos:*

“¿Cuánto es 30 JUS hoy?”
“¿Cuántos JUS son $2.000.000 en 2023?”

### 4. Presupuestos por servicio (core del sistema)

Presupuestos automáticos a partir del Código Arancelario:

- selección de uno o más servicios
- suma total en JUS
- conversión a pesos

Detalle por ítem:
- servicio
- cantidad de JUS
- fundamento legal
- subtotal y total

*Ejemplos:*

“Armame un presupuesto por divorcio bilateral con convenio regulador”
“Sumá consulta escrita + redacción de contrato”

### 5. Comparaciones temporales

Comparar:

- costo de un mismo servicio en distintas fechas
- evolución del valor del JUS

Mostrar:

- diferencia absoluta
- diferencia porcentual

*Ejemplos:*

“¿Cuánto aumentó el costo de un divorcio desde 2021 a hoy?”
“Compará 50 JUS en 2020 vs 2025”

### 6. Comportamiento por defecto

Provincia: Córdoba siempre

Fecha:

- “hoy / actual” → último valor publicado
- no indicada → último valor publicado

Moneda: pesos argentinos

Si un dato no está en la normativa:

- el sistema no infiere
- responde que no existe previsión expresa

### 7. Modelo de datos y metadata

Metadata mínima por documento/chunk

```
provincia: "Córdoba" (constante)
fecha_vigencia: YYYY-MM-DD
valor_jus: number | null
moneda: "ARS"
fuente:
    - nombre_documento
    - artículo / sección
    - URL o referencia oficial
tipo:
    - "valor_jus"
    - "normativa"
    - "tabla_servicios"
```

Notas:
- `provincia` no se infiere ni se parametriza, es siempre Córdoba

- `valor_jus` solo existe en documentos de tipo `valor_jus`

- Las tablas de servicios se moelan como normativa estructurada, no texto libre

### 8. Comportamiento del RAG

# Respuesta estándar

Toda respuesta debe devolver explícitamente:

- Respuesta (clara y directa).
- Provincia: Córdoba.
- Fecha del valor del JUS utilizado
    - indicada por el usuario, o
    - último valor vigente si no se indicó fecha.
- Fuente normativa
    - ley / artículo / tabla
    - referencia documental.

_Ejemplo de cierre de respuesta:_

Provincia: Córdoba
Valor del JUS utilizado: 01/12/2025
Fuente: Ley 9459, art. 70

# Manejo de información inexistente

Si el dato no está en el corpus:

- No inferir.
- No estimar.
- No “aproximar”.

_Respuesta obligatoria:_

"La normativa vigente de la Provincia de Córdoba no establece un valor en JUS para ese servicio."

Si se consulta por fuera de la provincia de Córdoba:

_Respuesta obligatoria:_

"Este sistema trabaja exclusivamente con la normativa vigente de la Provincia de Córdoba, por lo que no dispone de información normativa ni valores oficiales de JUS para otras provincias."

Si se pide asesoramiento legal:

_Respuesta obligatoria:_

"Este sistema se limita a informar valores, rangos y cálculos previstos en la normativa arancelaria vigente de la Provincia de Córdoba. Para este tipo de análisis corresponde la intervención de un profesional matriculado."

### 9. API

#### 1. Preguntas libres

`POST /ask`

- Provincia implícita: Córdoba.
- Usa RAG completo.
- Devuelve siempre respuesta + metadata.

## Funcionalidades excluidas

- Otras provincias
- Interpretación jurisprudencial
- Asesoramiento legal o estratégico
- Cálculos fuera del Código Arancelario

## Resultado

Un sistema:

- normativo
- determinístico
- trazable
- defendible técnicamente y legalmente

