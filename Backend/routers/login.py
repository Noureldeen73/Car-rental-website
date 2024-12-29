from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from Backend.database import get_db
import bcrypt


router = APIRouter(
    prefix = '/login',
    tags = ['login']
)

@router.get('/authenticate/')
async def authenticateLoginDetails(email: str, password: str, db=Depends(get_db)):
    # check if user exists with this email and password
    # if exists, return {user_id: user_id, is_admin: is_admin}
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    user = await db.fetchrow("""SELECT * FROM "User" WHERE email = $1 AND password = $2""", email, hashed_password_str)
    if user:
        return {"user_id": user['user_id'], "is_admin": user['is_admin']}
    else:
        raise HTTPException(status_code=400, detail="Invalid email or password")