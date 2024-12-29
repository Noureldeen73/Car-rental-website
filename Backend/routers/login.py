from fastapi import FastAPI, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import get_db


router = APIRouter(
    prefix = '/login',
    tags = ['login']
)

@router.get('/authenticate/')
async def authenticateLoginDetails(email: str, password: str, db=Depends(get_db)):
    # IMPLEMENT YA SHABAB 
    pass