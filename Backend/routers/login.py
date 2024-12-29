from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from Backend.database import get_db


router = APIRouter(
    prefix = '/login',
    tags = ['login']
)

@router.get('/authenticate/')
async def authenticateLoginDetails(email: str, password: str, db=Depends(get_db)):
    # IMPLEMENT YA SHABAB 
    # check if user exists with this email and password
    # if exists, return {user_id: user_id, is_admin: is_admin}
    pass