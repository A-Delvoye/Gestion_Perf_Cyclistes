from fastapi import FastAPI
from endpoints import auth

app = FastAPI(
    #lifespan=token_cleaner, 
    title="Gestion Perf Cycliste", 
    description="Service en ligne de gestion des preformances cyclistes")

# Inclure les routes définies dans les fichiers séparés
#app.include_router(auth.router, prefix="??", tags=["auth"])
app.include_router(auth.router)
