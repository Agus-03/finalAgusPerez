def classify_intent(question: str) -> str:
    q = question.lower()

    if any(w in q for w in ["me conviene", "recomendas", "recomienda"]):
        return "personal_advice"

    if any(w in q for w in ["valor del jus", "jus actualmente", "jus actual", "jus vigente"]):
        return "jus_actual"

    if "durante" in q or "histórico" in q or "año" in q:
        return "jus_historico"

    return "normativa"
