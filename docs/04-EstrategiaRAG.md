# Estrategia RAG  
**Sistema JUS – Provincia de Córdoba**

## 1. Objetivo
Definir la estrategia de recuperación y generación (RAG) del sistema, asegurando que:
- las respuestas sean correctas y trazables
- no se produzcan inferencias no fundadas
- la normativa prevalezca sobre cualquier otro contenido
- el sistema sea determinístico en sus decisiones

## 2. Principios rectores

1. **Primacía normativa**  
   La normativa expresa siempre prevalece sobre cualquier otro contenido.

2. **No inferencia**  
   El sistema no completa información ausente ni elige valores dentro de rangos.

3. **Separación de responsabilidades**  
   - El RAG recupera y fundamenta.
   - La lógica determinística calcula.
   - El modelo no realiza operaciones matemáticas.

4. **Citación obligatoria**  
   Toda respuesta debe estar respaldada por al menos una fuente del corpus.

## 3. Clasificación de consultas

Antes de recuperar información, la consulta del usuario se clasifica en uno o más de los siguientes tipos:

### 3.1 Consulta normativa
Ejemplos:
- “¿Cuántos JUS corresponde un divorcio bilateral?”
- “¿Qué dice la ley sobre consultas escritas?”

Prioridad de recuperación:
1. `tabla_servicios`
2. `normativa`

### 3.2 Consulta de valor del JUS
Ejemplos:
- “¿Cuánto vale el JUS hoy?”
- “Valor del JUS en 2022”

Prioridad de recuperación:
1. `valor_jus`

### 3.3 Consulta de cálculo
Ejemplos:
- “¿Cuánto es 30 JUS en pesos?”
- “Convertí $1.000.000 a JUS en 2023”

Prioridad de recuperación:
1. `valor_jus`  
Luego deriva a lógica determinística.

### 3.4 Presupuesto por servicios
Ejemplos:
- “Armame un presupuesto por divorcio bilateral”
- “Sumá consulta escrita y redacción de contrato”

Prioridad de recuperación:
1. `tabla_servicios`
2. `valor_jus`

### 3.5 Comparación temporal
Ejemplos:
- “¿Cuánto aumentó el divorcio desde 2020 a hoy?”

Prioridad de recuperación:
1. `tabla_servicios`
2. `valor_jus` (múltiples fechas)

### 3.6 Consulta fuera de dominio
Ejemplos:
- “Valor del JUS en Santa Fe”
- “Honorarios en otra provincia”

Resultado:
- respuesta de fuera de alcance
- no se realiza recuperación

### 3.7 Solicitud de asesoramiento
Ejemplos:
- “¿Me conviene iniciar este juicio?”
- “¿Qué me recomendás cobrar?”

Resultado:
- respuesta de rechazo por asesoramiento
- no se realiza recuperación

## 4. Estrategia de recuperación

### 4.1 Filtros obligatorios
Toda recuperación aplica los siguientes filtros:
- `provincia = Córdoba`
- `tipo` según la clasificación de la consulta

### 4.2 Orden de búsqueda
Cuando se buscan múltiples tipos de chunks, se respeta el siguiente orden:

1. `tabla_servicios`
2. `normativa`
3. `valor_jus`

Nunca se mezclan resultados sin jerarquía.

### 4.3 Top-k recomendado
- `tabla_servicios`: k = 3
- `normativa`: k = 5
- `valor_jus`: k = 1 por fecha solicitada

El objetivo no es variedad, sino **precisión**.

## 5. Manejo de conflictos

### 5.1 Conflicto entre normativa general y específica
- Gana la normativa específica del servicio.
- La normativa general solo se usa como complemento explicativo.

### 5.2 Servicios con rango de JUS
- El sistema informa el rango completo.
- No selecciona valores intermedios.
- No realiza estimaciones.

Ejemplo de respuesta válida:
> El servicio tiene un rango previsto entre 50 y 120 JUS según la Ley 9459, Art. XX.

### 5.3 Información inexistente
Si no existe un chunk aplicable:
- se informa ausencia normativa
- se explica qué dato falta
- no se infiere ni se completa

## 6. Prompt del sistema (comportamiento del modelo)

El modelo debe cumplir las siguientes reglas:

- responder exclusivamente con información recuperada del corpus
- no inferir valores no explícitos
- no brindar asesoramiento legal
- citar siempre la fuente normativa
- indicar provincia y fecha del valor del JUS cuando corresponda

## 7. Formato estándar de respuesta

Toda respuesta debe incluir:

- respuesta clara y directa
- provincia: Córdoba
- fecha del valor del JUS utilizado (si aplica)
- fuente normativa citada

## 8. Resultado esperado

Con esta estrategia:
- el sistema responde de forma consistente
- las respuestas son reproducibles
- no existen alucinaciones
- el comportamiento es defendible técnica y jurídicamente

Esta estrategia es independiente de la implementación técnica.
