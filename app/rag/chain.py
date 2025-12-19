from langchain_cohere import ChatCohere
from app.config import COHERE_API_KEY, LLM_MODEL
from app.rag.prompt import SYSTEM_PROMPT

def generate_answer(context: str, question: str):
    llm = ChatCohere(
        cohere_api_key=COHERE_API_KEY,
        model=LLM_MODEL,
        temperature=0
    )

    prompt = f"""
    {SYSTEM_PROMPT}

    Contexto:
    {context}

    Pregunta:
    {question}
    """

    return llm.invoke(prompt).content
