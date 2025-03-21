from fastapi import FastAPI
from endpoints import auth, cycliste, enregistrement, utilisateur,stats
from core.config import API_NAME, API_DESCRIPTION
from utils.lifespan_handler import token_cleaner

app = FastAPI(
    lifespan=token_cleaner, 
    title=API_NAME, 
    description=API_DESCRIPTION )

# Inclure les routes définies dans les fichiers séparés
app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(utilisateur.router, prefix="", tags=["utilisateur"])
app.include_router(cycliste.router, prefix="", tags=["cycliste"])
app.include_router(enregistrement.router, prefix="", tags=["enregistrement"])
app.include_router(stats.router, prefix="", tags=["stats"])



