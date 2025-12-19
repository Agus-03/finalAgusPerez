from langchain_community.vectorstores import Chroma
from langchain_cohere import CohereEmbeddings
from app.config import CHROMA_DIR, COHERE_API_KEY, EMBEDDING_MODEL

def get_vectorstore():
    embeddings = CohereEmbeddings(
        cohere_api_key=COHERE_API_KEY,
        model=EMBEDDING_MODEL
    )

    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )
