from app.db.chroma import get_vectorstore
from typing import Iterable


def retrieve(query: str, tipos: Iterable[str], k: int = 5):
    vs = get_vectorstore()

    tipos = list(tipos)

    filters = [{"provincia": "Córdoba"}]

    if len(tipos) == 1:
        filters.append({"tipo": tipos[0]})
    elif len(tipos) > 1:
        filters.append({
            "$or": [{"tipo": t} for t in tipos]
        })

    # Construcción segura del where
    if len(filters) == 1:
        where = filters[0]
    else:
        where = {"$and": filters}

    return vs.similarity_search(
        query,
        k=k,
        filter=where
    )
