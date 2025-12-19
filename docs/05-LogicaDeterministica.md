# Lógica Determinística  
**Sistema JUS – Provincia de Córdoba**

## 1. Objetivo
Definir todas las operaciones determinísticas del sistema, estableciendo:
- qué cálculos se realizan fuera del modelo de lenguaje
- qué reglas se aplican
- en qué casos no se puede calcular un resultado

El objetivo es garantizar:
- resultados reproducibles
- separación clara entre cálculo y lenguaje natural
- ausencia de decisiones arbitrarias

## 2. Principio general

Toda operación matemática o aritmética:
- **no es realizada por el LLM**
- se ejecuta mediante lógica determinística
- utiliza exclusivamente datos recuperados del corpus

El modelo de lenguaje:
- explica
- contextualiza
- cita la fuente  
pero **no calcula**.

## 3. Conversión JUS ↔ Pesos

### 3.1 Conversión de JUS a pesos
**Fórmula**
```text
monto_pesos = cantidad_jus × valor_jus_vigente
```

**Reglas:**
- `cantidad_jus` debe ser numérica
- `valor_jus_vigente` se obtiene de `ValorJus`
- si no se indica fecha: se usa el último valor vigente
- el resultado se expresa en ARS

### 3.2 Conversión de pesos a JUS
Fórmula
```text
cantidad_jus = monto_pesos ÷ valor_jus_vigente
```

**Reglas:**

- el resultado se informa con precisión decimal
- no se redondea salvo indicación expresa
- se informa siempre el valor del JUS utilizado

## 4. Cálculo de presupuestos
### 4.1 Presupuesto con servicios de JUS fijo
Condiciones:

- todos los servicios tienen valor fijo en JUS

**Cálculo**
```text
jus_total = Σ (jus_servicio × cantidad)
monto_pesos = jus_total × valor_jus
```

### 4.2 Servicios con rango de JUS
Condiciones:

- el servicio tiene mínimo y máximo normativo

**Regla:**

- el sistema no selecciona valores dentro del rango

- no se calcula total automático

**Resultado:**

- se informa el rango completo

- se indica que el presupuesto no es cuantificable automáticamente

### 4.3 Presupuestos mixtos
Condiciones:

- al menos un servicio tiene rango de JUS

**Regla:**

- el presupuesto completo se marca como no calculable

- se detallan los ítems cuantificables y no cuantificables

## 5. Comparaciones temporales
### 5.1 Comparación de valores en pesos
Condiciones:

- mismo servicio

- distintas fechas del valor del JUS

**Cálculos**
```text
diferencia_abs = valor_final - valor_inicial
diferencia_pct = (diferencia_abs ÷ valor_inicial) × 100
```

### 5.2 Restricciones

- no se comparan servicios distintos

-no se comparan provincias (fuera de alcance)

-si falta alguna fecha:

-no se realiza el cálculo

## 6. Manejo de errores y casos no calculables
### 6.1 Datos faltantes
Ejemplos:

- no existe valor del JUS para la fecha

- el servicio no está definido en la normativa

**Resultado**

- no se calcula

- se informa el motivo

### 6.2 Casos fuera de dominio
Ejemplos:

- otra provincia

- otra normativa

**Resultado**

- no se ejecuta lógica determinística

### 6.3 Solicitudes de asesoramiento
Ejemplos:

- elección de valor dentro de un rango

- recomendaciones estratégicas

**Resultado**

- no se calcula

- se responde con rechazo normativo

## 7. Relación con el RAG

El RAG:

- identifica el servicio

- recupera la normativa

- obtiene el valor del JUS

La lógica determinística:

- calcula

- valida

- retorna resultados numéricos

No existe lógica híbrida.

## 8. Resultado esperado
Con esta lógica:

- los cálculos son exactos
- el comportamiento es reproducible
- el sistema es auditable
- no hay inferencias matemáticas del LLM