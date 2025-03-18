from fastapi import FastAPI
from endpoints import auth
from core.config import API_NAME, API_DESCRIPTION

app = FastAPI(
    #lifespan=token_cleaner, 
    title=API_NAME, 
    description=API_DESCRIPTION )

# Inclure les routes définies dans les fichiers séparés
#app.include_router(auth.router, prefix="??", tags=["auth"])
app.include_router(auth.router)
