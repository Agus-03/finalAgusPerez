from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from pypdf import PdfReader
from langchain_core.documents import Document

from app.db.chroma import get_vectorstore


# ============================
# Configuración
# ============================

DEFAULT_RAW_DIR = Path("data/raw")

TIPO_NORMATIVA = "normativa"
TIPO_VALOR_JUS = "valor_jus"
TIPO_NORMATIVA_PROCESAL = "normativa_procesal"


@dataclass(frozen=True)
class Chunk:
    text: str
    metadata: dict


# ============================
# Helpers
# ============================

def read_pdf_text(pdf_path: Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = []
    for page in reader.pages:
        t = page.extract_text() or ""
        t = t.replace("\u00ad", "")  # soft hyphen típico de PDFs legales
        pages.append(t)
    return "\n".join(pages)


_ART_RE = re.compile(r"(?im)^\s*(Artículo|Art\.?)\s+(\d+)\.?\s*(.*)$")


def split_by_articles(text: str) -> list[tuple[str, str]]:
    """
    Divide el texto por Artículo N.
    Devuelve [(numero_articulo, texto_completo)]
    """
    lines = text.splitlines()
    indices = []

    for i, line in enumerate(lines):
        m = _ART_RE.match(line)
        if m:
            indices.append((i, m.group(2)))

    if not indices:
        return [("s/d", text.strip())]

    chunks = []
    for idx, (start, art_num) in enumerate(indices):
        end = indices[idx + 1][0] if idx + 1 < len(indices) else len(lines)
        block = "\n".join(lines[start:end]).strip()
        chunks.append((art_num, block))

    return chunks


# ============================
# Loaders
# ============================

def load_normativa_pdf(pdf_path: Path) -> list[Chunk]:
    full_text = read_pdf_text(pdf_path)
    articles = split_by_articles(full_text)

    # 🔹 Detectar si es Código Procesal
    is_procesal = any(
        kw in pdf_path.name.lower()
        for kw in ["procesal", "procedimiento", "cpcc"]
    )

    tipo = TIPO_NORMATIVA_PROCESAL if is_procesal else TIPO_NORMATIVA
    codigo = "CPCC" if is_procesal else "Ley 9459"

    out = []
    for art_num, block in articles:
        if not block:
            continue

        out.append(
            Chunk(
                text=block,
                metadata={
                    "provincia": "Córdoba",
                    "tipo": tipo,
                    "codigo": codigo,
                    "articulo": art_num,
                    "fecha_vigencia": None,
                    "valor_jus": None,
                    "fuente_nombre": pdf_path.name,
                    "fuente_referencia": (
                        f"{codigo}, Art. {art_num}"
                        if art_num != "s/d"
                        else codigo
                    ),
                },
            )
        )

    return out


def parse_date(value: str) -> str:
    value = value.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass
    raise ValueError(f"Fecha inválida: {value}")


def load_valor_jus_csv(csv_path: Path) -> list[Chunk]:
    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError("CSV sin encabezados")

        headers = {h.lower(): h for h in reader.fieldnames}
        fecha_col = headers.get("fecha") or headers.get("fecha_vigencia")
        valor_col = headers.get("valor_jus") or headers.get("valor")

        if not fecha_col or not valor_col:
            raise ValueError(
                f"CSV inválido. Encabezados encontrados: {reader.fieldnames}"
            )

        out = []
        for row in reader:
            fecha = parse_date(row[fecha_col])
            valor = float(str(row[valor_col]).replace(".", "").replace(",", "."))

            text = (
                "Valor del JUS – Provincia de Córdoba\n"
                f"Vigente desde: {fecha}\n"
                f"Valor: {valor}"
            )

            out.append(
                Chunk(
                    text=text,
                    metadata={
                        "provincia": "Córdoba",
                        "tipo": TIPO_VALOR_JUS,
                        "fecha_vigencia": fecha,
                        "valor_jus": valor,
                        "articulo": None,
                        "fuente_nombre": csv_path.name,
                        "fuente_referencia": "Tabla oficial del valor del JUS",
                    },
                )
            )

        return out


# ============================
# Persistencia
# ============================

def ingest_to_chroma(chunks: Iterable[Chunk], reset: bool = False):
    vs = get_vectorstore()

    if reset:
        try:
            vs._collection.delete(where={})  # MVP, borrado total
        except Exception:
            pass

    docs = [Document(page_content=c.text, metadata=c.metadata) for c in chunks]

    BATCH_SIZE = 20  # conservador para trial

    for i in range(0, len(docs), BATCH_SIZE):
        batch = docs[i : i + BATCH_SIZE]
        vs.add_documents(batch)


# ============================
# CLI
# ============================

def main():
    parser = argparse.ArgumentParser("Ingesta corpus JUS → Chroma")
    parser.add_argument("--raw-dir", default=str(DEFAULT_RAW_DIR))
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args()

    raw_dir = Path(args.raw_dir)
    if not raw_dir.exists():
        raise SystemExit(f"No existe {raw_dir.resolve()}")

    chunks: list[Chunk] = []

    # PDFs normativos
    for pdf in raw_dir.glob("*.pdf"):
        chunks.extend(load_normativa_pdf(pdf))

    # CSV valor JUS
    for csv_file in raw_dir.glob("*.csv"):
        if "jus" in csv_file.name.lower():
            chunks.extend(load_valor_jus_csv(csv_file))

    if not chunks:
        raise SystemExit("No se generaron chunks. Revisá data/raw.")

    ingest_to_chroma(chunks, reset=args.reset)
    print(f"OK: ingeridos {len(chunks)} chunks desde {raw_dir}")


if __name__ == "__main__":
    main()
