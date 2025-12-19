from app.db.chroma import get_vectorstore
from datetime import datetime
import csv
from pathlib import Path

JUS_CSV_PATH = Path("data/raw/valor_jus.csv")

def jus_to_pesos(jus: float, valor_jus: float) -> float:
    return jus * valor_jus

def get_jus_actual():
    """
    Devuelve SIEMPRE el valor vigente del JUS,
    tomando la PRIMERA fila del CSV.
    """
    with JUS_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        first_row = next(reader, None)

        if not first_row:
            return None, None

        fecha = first_row["fecha_vigencia"].strip()
        valor = float(
            str(first_row["valor_jus"]).replace(".", "").replace(",", ".")
        )

        return valor, fecha

def get_jus_por_anio(anio: int):
    """
    Devuelve todos los valores del JUS de un año,
    ordenados de más reciente a más antiguo.
    """
    valores = []

    with JUS_CSV_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            fecha = row["fecha_vigencia"].strip()
            if not fecha.startswith(str(anio)):
                continue

            valor = float(
                str(row["valor_jus"]).replace(".", "").replace(",", ".")
            )

            valores.append(
                {
                    "fecha_vigencia": fecha,
                    "valor_jus": valor,
                }
            )

    return valores

