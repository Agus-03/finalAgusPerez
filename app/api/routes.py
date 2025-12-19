from fastapi import APIRouter
from app.rag.retriever import retrieve
from app.rag.reranker import rerank
from app.rag.chain import generate_answer
from app.memory.history import save_message

import re
from app.logic.postprocess import enrich_with_pesos
from app.rag.intent import classify_intent
from app.logic.jus import get_jus_actual, get_jus_por_anio

router = APIRouter()

COST_KEYWORDS = [
    "cuanto cuesta", "costo", "precio",
    "arancel", "sale", "me cuesta"
]

# ============================
# Provincia / localidad
# ============================

def normalize_provincia(question: str):
    q = question.lower()

    provincias_no_cba = [
        "chaco", "santa fe", "buenos aires", "mendoza",
        "san juan", "san luis", "corrientes", "misiones",
        "salta", "jujuy", "formosa", "tucuman", "neuquen",
        "rio negro", "chubut", "santa cruz", "la pampa",
        "entre rios", "catamarca", "la rioja",
        "santiago del estero", "tierra del fuego"
    ]

    for p in provincias_no_cba:
        if p in q:
            return "OTRA_PROVINCIA"

    localidades_cba = [
        "Achiras", "Adelia María", "Agua de Oro", "Alcira Gigena", "Aldea Santa María", 
        "Alejandro Roca", "Alejo Ledesma", "Alicia", "Almafuerte", "Alpa Corral", 
        "Alta Gracia", "Alto de los Quebrachos", "Altos de Chipión", "Amboy", "Ambul", 
        "Ana Zumarán", "Anisacate", "Arguello", "Arias", "Arroyito", "Arroyo Algodón", 
        "Arroyo Cabral", "Arroyo Los Patos", "Assunta", "Atahona", "Ausonia", 
        "Avellaneda", "Ballesteros", "Ballesteros Sud", "Balnearia", "Bañado de Soto", 
        "Bell Ville", "Bengolea", "Benjamín Gould", "Berrotarán", "Bialet Massé", 
        "Bouwer", "Brinkmann", "Buchardo", "Bulnes", "Cabalango", "Calchín", 
        "Calchín Oeste", "Calmayo", "Camilo Aldao", "Caminiaga", "Cañada de Luque", 
        "Cañada de Machado", "Cañada de Río Pinto", "Cañada del Sauce", "Canals", 
        "Candelaria Sud", "Capilla de los Remedios", "Capilla de Sitón", 
        "Capilla del Carmen", "Capilla del Monte", "Capitán General Bernardo O'Higgins", 
        "Carnerillo", "Carrilobo", "Casa Grande", "Cavanagh", "Cerro Colorado", 
        "Chaján", "Chalacea", "Chazón", "Chilibroste", "Chucul", "Chuña", 
        "Chuña Huasi", "Churqui Cañada", "Ciénaga Del Coro", "Cintra", "Colazo", 
        "Colonia Almada", "Colonia Anita", "Colonia Barge", "Colonia Bismark", 
        "Colonia Bremen", "Colonia Caroya", "Colonia Italiana", "Colonia Iturraspe", 
        "Colonia Las Cuatro Esquinas", "Colonia Las Pichanas", "Colonia Marina", 
        "Colonia Prosperidad", "Colonia San Bartolomé", "Colonia San Pedro", 
        "Colonia Tirolesa", "Colonia Vicente Agüero", "Colonia Videla", 
        "Colonia Vignaud", "Colonia Waltelina", "Comechingones", "Conlara", 
        "Copacabana", "Córdoba", "Coronel Baigorria", "Coronel Moldes", 
        "Corral de Bustos", "Corralito", "Cosquín", "Costa Sacate", "Cruz Alta", 
        "Cruz de Caña", "Cruz del Eje", "Cuesta Blanca", "Dean Funes", "Del Campillo", 
        "Despeñaderos", "Devoto", "Diego de Rojas", "Dique Chico", "El Arañado", 
        "El Brete", "El Chacho", "El Fortín", "El Manzano", "El Rastreador", 
        "El Rodeo", "El Tío", "Elena", "Embalse", "Esquina", "Estación General Paz", 
        "Estación Juárez Celman", "Estancia de Guadalupe", "Estancia Vieja", 
        "Etruria", "Eufrasio Loza", "Falda del Carmen", "Freyre", "General Baldissera", 
        "General Cabrera", "General Deheza", "General Fotheringham", "General Levalle", 
        "General Roca", "Guanaco Muerto", "Guasapampa", "Guatimozín", "Gutenberg", 
        "Hernando", "Huanchilla", "Huerta Grande", "Huincar Renancó", "Idiazábal", 
        "Impira", "Inriville", "Isla Verde", "Italo", "James Craik", "Jesús María", 
        "Jovita", "Justiniano Posse", "Kilómetro 658", "L. V. Mansilla", "La Batea", 
        "La Calera", "La Carlota", "La Carolina", "La Cautiva", "La Cesira", 
        "La Cruz", "La Cumbre", "La Cumbrecita", "La Falda", "La Francia", 
        "La Granja", "La Higuera", "La Laguna", "La Paisanita", "La Palestina", 
        "La Pampa", "La Paquita", "La Para", "La Paz", "La Playa", "La Playosa", 
        "La Población", "La Posta", "La Puerta", "La Quinta", "La Rancherita", 
        "La Rinconada", "La Serranita", "La Tordilla", "Laborde", "Laboulaye", 
        "Laguna Larga", "Las Acequias", "Las Albahacas", "Las Arrias", "Las Bajadas", 
        "Las Caleras", "Las Calles", "Las Cañadas", "Las Gramillas", "Las Higueras", 
        "Las Isletillas", "Las Junturas", "Las Palmas", "Las Peñas", 
        "Las Peñas Sud", "Las Perdices", "Las Playas", "Las Rabonas", "Las Saladas", 
        "Las Tapias", "Las Varas", "Las Varillas", "Las Vertientes", "Leguizamón", 
        "Leones", "Los Cedros", "Los Cerrillos", "Los Chañaritos", "Los Cisnes", 
        "Los Cocos", "Los Cóndores", "Los Hornillos", "Los Hoyos", "Los Mistoles", 
        "Los Molinos", "Los Pozos", "Los Reartes", "Los Surgentes", "Los Talares", 
        "Los Zorros", "Lozada", "Luca", "Lucio V. Mansilla", "Luque", "Luyaba", 
        "Malagueño", "Malena", "Malvinas Argentinas", "Manfredi", "Maquinista Gallini", 
        "Marcos Juárez", "Marull", "Matorrales", "Mattaldi", "Mayu Sumaj", 
        "Media Naranja", "Melo", "Mendiolaza", "Mi Granja", "Mina Clavero", 
        "Miramar", "Monte Buey", "Monte Cristo", "Monte De Los Gauchos", "Monte Leña", 
        "Monte Maíz", "Monte Ralo", "Morrison", "Morteros", "Nicolás Bruzzone", 
        "Noetinger", "Nono", "Olaeta", "Oliva", "Onagoity", "Oncativo", "Ordoñez", 
        "Pacheco De Melo", "Pampayasta Norte", "Pampayasta Sud", "Panaholma", 
        "Pascanas", "Pasco", "Paso del Durazno", "Paso Viejo", "Pilar", "Pincén", 
        "Piquillín", "Plaza de Mercedes", "Plaza Luxardo", "Porteña", 
        "Potrero de Garay", "Pozo del Molle", "Pozo Nuevo", "Pueblo Italiano", 
        "Puesto de Castro", "Punta del Agua", "Quebracho Herrado", "Quilino", 
        "Rafael García", "Ranqueles", "Rayo Cortado", "Reducción", "Rincón", 
        "Río Bamba", "Río Ceballos", "Río Cuarto", "Río de Los Sauces", "Río Primero", 
        "Río Segundo", "Río Tercero", "Rosales", "Rosario del Saladillo", 
        "Sacanta", "Sagrada Familia", "Saira", "Saladillo", "Saldán", "Salsacate", 
        "Salsipuedes", "Sampacho", "San Agustín", "San Antonio de Arredondo", 
        "San Antonio de Litín", "San Basilio", "San Carlos Minas", "San Clemente", 
        "San Esteban", "San Francisco", "San Francisco del Chañar", "San Gerónimo", 
        "San Ignacio", "San Javier", "San Joaquín", "San José", "San José de La Dormida", 
        "San José de Las Salinas", "San Lorenzo", "San Marcos Sierras", 
        "San Marcos Sud", "San Pedro", "San Pedro Norte", "San Roque", 
        "San Vicente", "Santa Catalina", "Santa Eufemia", "Santa María de Punilla", 
        "Santa Mónica", "Santa Rosa de Calamuchita", "Santa Rosa de Río Primero", 
        "Santiago Temple", "Sarmiento", "Saturnino M. Laspiur", "Sauce Arriba", 
        "Sebastián Elcano", "Seeber", "Segunda Usina", "Serrano", "Serrezuela", 
        "Sinsacate", "Suco", "Tala Cañada", "Tala Huasi", "Talaini", "Tancacha", 
        "Tanti", "Ticino", "Tinoco", "Tío Pujio", "Toledo", "Toro Pujio", 
        "Tosno", "Tosquita", "Tránsito", "Tuclame", "Ucacha", "Unquillo", 
        "Valle de Anisacate", "Valle Hermoso", "Viamonte", "Vicuña Mackenna", 
        "Villa Allende", "Villa Amancay", "Villa Ascasubi", "Villa Candelaria Norte", 
        "Villa Carlos Paz", "Villa Cerro Azul", "Villa Ciudad de América", 
        "Villa Ciudad Parque", "Villa Concepción del Tío", "Villa Cura Brochero", 
        "Villa de Las Rosas", "Villa de María", "Villa de Pocho", "Villa de Soto", 
        "Villa del Dique", "Villa del Prado", "Villa del Rosario", "Villa del Totoral", 
        "Villa Dolores", "Villa El Chacay", "Villa Elisa", "Villa Flor Serrana", 
        "Villa Fontana", "Villa General Belgrano", "Villa Giardino", "Villa Huidobro", 
        "Villa La Bolsa", "Villa Los Aromos", "Villa Los Patos", "Villa María", 
        "Villa Nueva", "Villa Parque Santa Ana", "Villa Parque Siquiman", 
        "Villa Quillinzo", "Villa Rossi", "Villa Rumipal", "Villa San Esteban", 
        "Villa San Isidro", "Villa Santa Cruz", "Villa Sarmiento", "Villa Tulumba", 
        "Villa Valeria", "Villa Yacanto", "Washington", "Wenceslao Escalante", 
        "Yacanto"
    ]

    if any(loc in q for loc in localidades_cba):
        return "CORDOBA_LOCALIDAD"

    if "cordoba" in q or "córdoba" in q:
        return "CORDOBA"

    return None


# ============================
# Endpoint principal
# ============================

@router.post("/ask")
def ask(question: str, session_id: str):

    intent = classify_intent(question)
    q = question.lower()

    # ------------------------
    # Provincia
    # ------------------------

    provincia = normalize_provincia(question)

    if provincia == "OTRA_PROVINCIA":
        return {
            "respuesta": (
                "No tengo información para esa provincia. "
                "Este sistema aplica únicamente a la Provincia de Córdoba."
            )
        }


    aclaracion_localidad = ""
    if provincia == "CORDOBA_LOCALIDAD":
        aclaracion_loclidad = (
            " El valor del JUS es único para toda la provincia de Córdoba."
        )   

    # ------------------------
    # Intenciones directas
    # ------------------------

    if intent == "personal_advice":
        return {
            "respuesta": "No puedo brindar recomendaciones personales ni asesoramiento jurídico."
        }

    if intent == "jus_actual":
        valor, fecha = get_jus_actual()
        texto = (
            f"El valor vigente del JUS en la Provincia de Córdoba es ${valor}, "
            f"vigente desde {fecha}. "
        )
        if aclaracion_localidad:
            texto += "El valor del JUS es único para toda la provincia."
        return {"respuesta": texto}

    if intent == "jus_historico":
        match = re.search(r"(20\d{2})", question)
        if not match:
            return {"respuesta": "Indicá el año que querés consultar."}

        anio = int(match.group(1))
        valores = get_jus_por_anio(anio)

        texto = f"Durante el año {anio} el valor del JUS en Córdoba fue:\n"
        for v in valores:
            texto += f"- Desde {v['fecha_vigencia']}: ${v['valor_jus']}\n"

        return {"respuesta": texto}

    # ------------------------
    # REGLA DE NEGOCIO
    # Costo ⇒ SOLO Código Arancelario
    # ------------------------

    if any(w in q for w in [
        "cuanto cuesta", "costo", "precio",
        "honorarios", "arancel", "sale", "me cuesta"
    ]):
        tipos = ["normativa"]

    # ------------------------
    # Procesal (solo si NO es costo)
    # ------------------------

    elif any(w in q for w in [
        "proceso", "procesal", "audiencia",
        "incidente", "recurso", "plazo",
        "etapa", "trámite", "tramite"
    ]):
        tipos = ["normativa_procesal"]

    else:
        tipos = ["normativa"]

    # ------------------------
    # RAG
    # ------------------------

    if any(k in q for k in COST_KEYWORDS):
        return {
            "respuesta": (
                "Según el Código Arancelario de la Provincia de Córdoba, "
                "los honorarios se expresan en JUS y dependen del tipo de trámite, "
                "su complejidad y la etapa procesal. "
                "Puedo indicarte el rango en JUS aplicable si precisás el trámite."
            )
        }

    docs = retrieve(question, tipos=tipos, k=5)
    docs = rerank(question, docs)

    context = "\n\n".join(d.page_content for d in docs)
    answer = generate_answer(context, question)
    answer = enrich_with_pesos(answer)

    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

    return {
        "respuesta": answer,
        "provincia": "Córdoba"
    }
