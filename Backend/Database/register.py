from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import get_db
import module

router = APIRouter(
    prefix = '/register',
    tags = ['register']
)

@router.post('/create_user/')
async def create_user(email: str, password: str, admin: bool = False, db=Depends(get_db)):
    try:
        await db.execute(
            """INSERT INTO "User" (email, password, is_admin) VALUES ($1, $2, $3)""",
            email, password, admin,
        )
        return {"email": email, "password": password, "admin": admin}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))