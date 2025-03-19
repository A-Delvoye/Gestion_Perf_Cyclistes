from fastapi import APIRouter, Depends, HTTPException
from sqlite3 import Connection
from app.db.creation_bdd import get_db_connection
from app.schemas.user import UserCreate, UserRead
from app.utils.security import get_password_hash

router = APIRouter()

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Connection = Depends(get_db_connection)):
    hashed_password = get_password_hash(user.password)
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", (user.username, hashed_password, user.role))
    db.commit()
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    db_user = cursor.fetchone()
    return UserRead(id=db_user[0], username=db_user[1], role=db_user[3], is_active=db_user[4])

@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Connection = Depends(get_db_connection)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    db_user = cursor.fetchone()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead(id=db_user[0], username=db_user[1], role=db_user[3], is_active=db_user[4])

