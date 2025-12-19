# Diseño del Corpus RAG

**Sistema JUS – Provincia de Córdoba**

## 1. Objetivo
Definir la estructura, segmentación y normalización del corpus documental que será utilizado por el sistema RAG, garantizando:
- trazabilidad normativa
- recuperación precisa
- ausencia de inferencias no fundadas

El corpus se limita **exclusivamente** a la Provincia de Córdoba.

## 2. Tipos de documentos del corpus

Todo el contenido se clasifica explícitamente en uno de los siguientes tipos.  
No se permite contenido sin tipo.

### 2.1 Normativa (`normativa`)
Incluye:
- Código Arancelario – Ley 9459
- modificaciones legales vigentes
- artículos, incisos y disposiciones generales

Uso:
- fundamentación legal
- respuestas normativas
- citas de artículos

### 2.2 Tabla de servicios (`tabla_servicios`)
Incluye:
- servicios profesionales expresamente definidos en la normativa
- valores fijos o rangos en JUS
- condiciones de aplicación del servicio

Uso:
- presupuestos
- determinación de JUS por servicio

### 2.3 Valor del JUS (`valor_jus`)
Incluye:
- tabla histórica del valor del JUS en Córdoba
- fechas de vigencia oficiales
- fuentes de publicación

Uso:
- conversiones JUS ↔ pesos
- comparaciones temporales

## 3. Definición de chunk

El corpus se segmenta en unidades mínimas denominadas *chunks*.  
Cada chunk debe ser:
- autocontenido
- citables de forma independiente
- asociado a una única fuente normativa o dato oficial

### 3.1 Chunk de normativa
- 1 artículo = 1 chunk
- artículos extensos pueden subdividirse por inciso
- el texto legal no se resume ni se interpreta

Ejemplo:

```
Ley 9459 – Artículo 70
Divorcio sin homologación de convenio regulador
Texto completo del artículo
```

### 3.2 Chunk de tabla de servicios
- 1 servicio = 1 chunk
- incluye exclusivamente:
  - nombre normalizado del servicio
  - valor en JUS (fijo o rango)
  - referencia normativa exacta

Ejemplo:

```
Servicio: Divorcio bilateral
JUS: 50
Fundamento: Ley 9459, Art. 70
```

### 3.3 Chunk de valor del JUS
- 1 fecha de vigencia = 1 chunk
- no se agrupan períodos
- la fecha debe ser explícita

Ejemplo:

```
Valor del JUS – Córdoba
Vigente desde: 2025-05-01
Valor: 44330
Fuente: Tribunal Superior de Justicia de Córdoba
```

## 4. Normalización del contenido

### 4.1 Servicios
- nombres únicos y consistentes
- sin sinónimos en el nombre principal
- los sinónimos se registran solo como metadata

Ejemplo:
- Correcto: **Divorcio bilateral**
- Incorrecto: Divorcio de común acuerdo / Divorcio bilateral

### 4.2 Fechas
- formato único: `YYYY-MM-DD`
- no se permiten expresiones relativas (“actual”, “vigente”, etc.)

### 4.3 Valores JUS
- numéricos
- sin símbolos
- sin texto descriptivo

## 5. Metadata mínima por chunk

Todo chunk debe incluir la siguiente metadata:

```yaml
provincia: "Córdoba"
tipo: "normativa" | "tabla_servicios" | "valor_jus"
fecha_vigencia: YYYY-MM-DD | null
servicio_codigo: string | null
articulo: string | null
valor_jus: number | null
fuente:
  nombre: string
  referencia: string
```

**Regla:**

Un chunk que no puede ser citado correctamente se considera inválido.

## 6. Restricciones explícitas

No se incluye en el corpus:

- interpretación doctrinaria
 
- jurisprudencia
 
- opiniones
 
- ejemplos no normativos

- valores estimados o inferidos

El corpus contiene exclusivamente norma y datos oficiales.

## 7. Resultado esperado

Al finalizar la preparación del corpus:

- cada servicio es recuperable de forma directa

- cada valor del JUS es trazable por fecha

- el sistema RAG no necesita inferir ni completar información

- toda respuesta puede citar su fuente normativa

Este diseño es previo e independiente de la implementación técnica.