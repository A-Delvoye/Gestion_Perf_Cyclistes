from fastapi import FastAPI
from contextlib import asynccontextmanager
from db.token_white_list import clean_tokens
from db.db_session import DB_Session

# Gestionnaire de lifespan asynchrone
@asynccontextmanager
async def token_cleaner(app: FastAPI):
    clean_tokens()  
    yield  