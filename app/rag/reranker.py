import cohere
from app.config import COHERE_API_KEY, RERANK_MODEL

co = cohere.Client(COHERE_API_KEY)

def rerank(query: str, docs: list, top_n: int = 3):
    response = co.rerank(
        model=RERANK_MODEL,
        query=query,
        documents=[d.page_content for d in docs],
        top_n=top_n
    )

    ranked_docs = []
    for item in response.results:
        # SDK nuevo: objeto con atributo index
        if hasattr(item, "index"):
            ranked_docs.append(docs[item.index])
        # SDK viejo: dict
        elif isinstance(item, dict) and "index" in item:
            ranked_docs.append(docs[item["index"]])

    return ranked_docs
