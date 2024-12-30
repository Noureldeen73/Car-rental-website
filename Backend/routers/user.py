from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from Backend.database import get_db
import Backend.module

router = APIRouter(
    prefix = '/user',
    tags = ['user']
)

@router.get("/users/{id}")
async def get_user(id: int, db=Depends(get_db)):
    try:
        user = await db.fetchrow("""SELECT * FROM "User" WHERE user_id = $1""", id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(user)  # Convert asyncpg record to dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/admin_id_by_user_id")
async def get_admin(user_id: int, db=Depends(get_db)):
    try:
        admin = await db.fetchrow("""SELECT admin_id FROM Admin WHERE user_id = $1""", user_id)
        if not admin:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(admin)  # Convert asyncpg record to dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/customer_id_by_user_id")
async def get_admin(user_id: int, db=Depends(get_db)):
    try:
        customer = await db.fetchrow("""SELECT customer_id FROM Customer WHERE user_id = $1""", user_id)
        if not customer:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(customer)  # Convert asyncpg record to dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))