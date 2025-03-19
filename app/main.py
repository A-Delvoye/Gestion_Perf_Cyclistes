from fastapi import FastAPI
# from app.api.endpoints import cyclists, users, auth
from app.db.creation_bdd import init_db, drop_all_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    drop_all_tables()
    init_db()

# app.include_router(cyclists.router, prefix="/api/v1/cyclists", tags=["cyclists"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])

