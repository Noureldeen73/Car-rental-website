from symtable import Class

from fastapi import FastAPI, HTTPException
import asyncpg
from pydantic import BaseModel
from fastapi import Depends
from sqlalchemy.orm import Session

app = FastAPI()

DATABASE_URL = "postgresql://postgres:nourysushi@localhost:5432/Car rental"

async def get_db() :
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

class User(BaseModel):
    id: int
    email: str
    password: str
    admin : bool
@app.post("/users/")
async def create_user(id : int, email: str, password: str, admin: bool,db: Session = Depends(get_db)):
    try :
        await db.execute("""INSERT INTO "User" (user_id, email, password, is_admin) VALUES ($1, $2, $3, $4)""", id, email, password, admin)
        return {"id": id, "email": email, "password": password, "admin": admin}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
app.get("/users/{id}")
async def get_user(id: int):
    try:
        user = await get_db().fetchrow("SELECT * FROM users WHERE id = $1", id)
        return user
    except Exception as e:
        raise HTTPException(status_code=410, detail=str(e))
