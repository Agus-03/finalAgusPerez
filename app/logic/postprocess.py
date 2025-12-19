import re
from app.logic.jus import get_jus_actual, jus_to_pesos

JUS_REGEX = re.compile(r"(\d+(?:[.,]\d+)?)\s*jus", re.IGNORECASE)

def enrich_with_pesos(text: str) -> str:
    """
    Detecta valores expresados en JUS dentro del texto y
    agrega la equivalencia en pesos usando el valor vigente.
    """
    matches = JUS_REGEX.findall(text)
    if not matches:
        return text

    valor_jus, fecha = get_jus_actual()
    if not valor_jus:
        return text

    lineas = []

    for m in matches:
        cantidad_jus = float(m.replace(",", "."))
        pesos = jus_to_pesos(cantidad_jus, valor_jus)

        lineas.append(
            f"- {cantidad_jus} JUS equivalen aproximadamente a ${round(pesos, 2)}"
        )

    agregado = (
        "\n\nEquivalencia en pesos "
        f"(valor del JUS vigente desde {fecha}):\n"
        + "\n".join(lineas)
        + "\n\n*El monto en pesos es estimado y puede variar si el valor del JUS se actualiza.*"
    )

    return text + agregado
