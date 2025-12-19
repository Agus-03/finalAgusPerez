from dotenv import load_dotenv
load_dotenv()

import os

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

CHROMA_DIR = "data/processed/chroma"
SQLITE_DB = "data/processed/conversations.db"

EMBEDDING_MODEL = "embed-multilingual-v3.0"
LLM_MODEL = "command-r-plus-08-2024"
RERANK_MODEL = "rerank-multilingual-v3.0"
