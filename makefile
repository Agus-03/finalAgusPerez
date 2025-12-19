# =====================
# Configuración
# =====================

VENV=.venv
PYTHON=$(VENV)/Scripts/python.exe
PIP=$(VENV)/Scripts/pip.exe

APP_MODULE=app.main:app
RAW_DIR=data/raw

# =====================
# Targets
# =====================

.PHONY: help venv install ingest ingest-reset run all clean

help:
	@echo "Comandos disponibles:"
	@echo "  make venv           -> crea el entorno virtual"
	@echo "  make install        -> instala dependencias"
	@echo "  make ingest         -> ingesta PDF + CSV en Chroma"
	@echo "  make ingest-reset   -> borra Chroma y reingesta"
	@echo "  make run            -> levanta la API"
	@echo "  make all            -> install + ingest + run"
	@echo "  make clean          -> borra venv y datos procesados"

# ---------------------
# Entorno
# ---------------------

venv:
	if exist $(VENV) rmdir /s /q $(VENV)
	py -3 -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r requirements.txt

# ---------------------
# Ingesta
# ---------------------

ingest:
	$(PYTHON) -m app.rag.ingest --raw-dir $(RAW_DIR)

ingest-reset:
	$(PYTHON) -m app.rag.ingest --raw-dir $(RAW_DIR) --reset

# ---------------------
# API
# ---------------------

run:
	$(PYTHON) -m uvicorn $(APP_MODULE) --reload

# ---------------------
# Todo junto
# ---------------------

all: install ingest run

# ---------------------
# Limpieza
# ---------------------

clean:
	if exist $(VENV) rmdir /s /q $(VENV)
	if exist data\processed rmdir /s /q data\processed
