# Modelo de datos canónico

**Sistema JUS – Provincia de Córdoba**

### Principios de diseño

- Provincia fija: Córdoba (no se parametriza).

- JUS como unidad primaria; pesos siempre derivados.

- Normativa explícita: todo dato debe tener respaldo legal.

- Determinismo: los cálculos no dependen del LLM.

### 1. Entidad: ValorJus

Representa el valor oficial del JUS para una fecha determinada.

```
ValorJus:
  fecha_vigencia: YYYY-MM-DD
  valor_jus: number
  moneda: "ARS"
  fuente:
    tipo: "resolucion" | "publicacion_oficial"
    referencia: string
    url: string | null
```

__Reglas:__

- Una fecha → un solo valor válido.

- El valor nunca disminuye (según ley).

- Si no se especifica fecha en una consulta: se usa el último valor vigente.

### 2. Entidad: ServicioArancelario

Representa un servicio profesional definido en el Código Arancelario.

```
ServicioArancelario:
  codigo: string
  nombre: string
  jus:
    tipo: "fijo" | "rango"
    minimo: number | null
    maximo: number | null
    fijo: number | null
  articulo:
    ley: "Ley 9459"
    articulo: string
  observaciones: string | null
```

_Ejemplos de uso:_

- Divorcio bilateral → JUS fijo.

- Procesos con rango → se informa el rango, no se decide arbitrariamente.

__Regla crítica:__

Si el servicio tiene rango de JUS, el sistema:

- informa el rango

- no elige un valor

- deja constancia normativa

### 3. Entidad: ItemPresupuesto

Elemento individual dentro de un presupuesto.

```
ItemPresupuesto:
  servicio_codigo: string
  servicio_nombre: string
  cantidad: number
  jus_unitario: number | null
  jus_total: number | null
  fundamento:
    ley: "Ley 9459"
    articulo: string
```

__Reglas:__

- `jus_unitario` solo existe si el servicio tiene valor fijo.

- Si el servicio es por rango: el item se marca como no cuantificable automáticamente.

### 4. Entidad: Presupuesto

Resultado agregado de uno o más servicios.

```
Presupuesto:
  fecha_jus_utilizada: YYYY-MM-DD
  valor_jus_utilizado: number
  items: ItemPresupuesto[]
  total_jus: number | null
  total_pesos: number | null
  fuente_valor_jus: referencia
```

__Reglas:__

Si algún ítem no es cuantificable:

- no se calcula total

- se informa el motivo

Si todos los ítems son válidos:

- total en JUS

- conversión a pesos

5. Entidad: RespuestaSistema

Formato estándar de salida del sistema.

```
RespuestaSistema:
  respuesta: string
  provincia: "Córdoba"
  fecha_valor_jus: YYYY-MM-DD | null
  fuentes:
    - referencia
```

__Regla:__

Toda respuesta debe mapear a esta estructura, incluso errores o rechazos.

### 6. Estados de respuesta no-calculable
`Fuera de dominio`
Motivo: Jurisdicción no soportada

`Silencio normativo`
Motivo: Servicio no definido en la normativa

`Asesoramiento legal`
Motivo: Consulta de carácter profesional o estratégico