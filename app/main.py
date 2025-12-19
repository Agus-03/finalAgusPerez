from fastapi import FastAPI
from app.api.routes import router
from app.memory.history import init_db

app = FastAPI(title="Sistema JUS Córdoba")
app.include_router(router)

@app.on_event("startup")
def startup():
    init_db()