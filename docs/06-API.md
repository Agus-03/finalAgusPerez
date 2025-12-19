# API  
**Sistema JUS – Provincia de Córdoba**

## 1. Objetivo
Definir la interfaz de programación (API) del sistema, estableciendo:
- endpoints disponibles
- formato de requests y responses
- comportamiento esperado
- manejo de errores y casos fuera de alcance

La API expone **exclusivamente** funcionalidades dentro del dominio del sistema.

## 2. Convenciones generales

- Provincia implícita: **Córdoba**
- Moneda: ARS
- Fechas en formato: `YYYY-MM-DD`
- Todas las respuestas incluyen:
  - provincia
  - fuentes normativas
- La API no brinda asesoramiento legal.

## 3. Endpoint: Preguntas libres

### `POST /ask`

Permite realizar consultas en lenguaje natural.

**Request**
```json
{
  "question": "string"
}
```

**Comportamiento**
- Clasifica la consulta

- Ejecuta recuperación RAG si corresponde

- Deriva a lógica determinística cuando hay cálculos

- Rechaza consultas fuera de alcance

**Response**

```json
{
  "respuesta": "string",
  "provincia": "Córdoba",
  "fecha_valor_jus": "YYYY-MM-DD | null",
  "fuentes": [
    {
      "referencia": "Ley 9459, Art. 70"
    }
  ]
}
```

## 4. Endpoint: Valor del JUS

`GET /jus/value`
Obtiene el valor del JUS para una fecha determinada.

**Query params**
- `fecha` (opcional): `YYYY-MM-DD`

**Comportamiento**
- Si no se indica fecha, devuelve el último valor vigente

- Si la fecha no existe, informa ausencia de datos

**Response**
```json
{
  "provincia": "Córdoba",
  "fecha_vigencia": "YYYY-MM-DD",
  "valor_jus": 44330,
  "moneda": "ARS",
  "fuente": {
    "referencia": "Publicación TSJ Córdoba"
  }
}
```

## 5. Endpoint: Conversión JUS ↔ Pesos
`POST /calc`

Realiza conversiones monetarias basadas en el valor del JUS.

**Request**
```json
{
  "fecha": "YYYY-MM-DD | null",
  "jus": 30,
  "pesos": null
}
```

Reglas:

- Se debe enviar solo uno de los campos jus o pesos

- Si no se indica fecha, se usa el último valor vigente

**Response**
```json
{
  "provincia": "Córdoba",
  "fecha_valor_jus": "YYYY-MM-DD",
  "valor_jus": 44330,
  "resultado": {
    "jus": 30,
    "pesos": 1329900
  },
  "fuente": {
    "referencia": "Publicación TSJ Córdoba"
  }
}
```

## 6. Endpoint: Presupuestos por servicios
`POST /quote`

Genera presupuestos automáticos a partir de servicios arancelarios.

**Request**
```json
{
  "fecha": "YYYY-MM-DD | null",
  "items": [
    {
      "servicio": "Divorcio bilateral",
      "cantidad": 1
    }
  ]
}
```

**Comportamiento **

- Recupera servicios del corpus

- Verifica si son cuantificables

- Calcula totales solo si todos los ítems tienen JUS fijo

**Response (cuantificable)**
```json
{
  "provincia": "Córdoba",
  "fecha_valor_jus": "YYYY-MM-DD",
  "valor_jus": 44330,
  "items": [
    {
      "servicio": "Divorcio bilateral",
      "cantidad": 1,
      "jus_unitario": 50,
      "jus_total": 50,
      "fundamento": "Ley 9459, Art. 70"
    }
  ],
  "total_jus": 50,
  "total_pesos": 2216500,
  "fuentes": [
    {
      "referencia": "Ley 9459, Art. 70"
    }
  ]
}
```

**Response (no cuantificable)**
```json
{
  "provincia": "Córdoba",
  "error": "El presupuesto no es cuantificable automáticamente",
  "detalle": "Uno o más servicios tienen rango de JUS",
  "fuentes": [
    {
      "referencia": "Ley 9459"
    }
  ]
}
```

## 7. Endpoint: Comparaciones temporales
`GET /compare`

Compara el valor en pesos de un servicio entre dos fechas.

**Query params**

- `servicio`: string

- `from`: YYYY-MM-DD

- `to`: YYYY-MM-DD

**Response**
```
{
  "provincia": "Córdoba",
  "servicio": "Divorcio bilateral",
  "jus": 50,
  "from": {
    "fecha": "2020-01-01",
    "valor_pesos": 350000
  },
  "to": {
    "fecha": "2025-05-01",
    "valor_pesos": 2216500
  },
  "diferencia_absoluta": 1866500,
  "diferencia_porcentual": 533.28,
  "fuentes": [
    {
      "referencia": "Ley 9459, Art. 70"
    }
  ]
}
```

## 8. Manejo de errores
**Fuera de dominio**
```json
{
  "error": "Consulta fuera del alcance del sistema",
  "detalle": "El sistema opera exclusivamente sobre la Provincia de Córdoba"
}
```
**Asesoramiento legal**
```json
{
  "error": "Consulta de carácter profesional",
  "detalle": "El sistema no brinda asesoramiento legal"
}
```

## 9. Resultado

Esta API:

- refleja exactamente el alcance funcional

- es consistente con el modelo de datos

- separa RAG de lógica determinística

- es auditable y defendible