from fastapi import FastAPI, HTTPException, APIRouter, Depends
from Backend.database import get_db
import bcrypt

router = APIRouter(
    prefix = '/login',
    tags = ['login']
)

@router.get('/authenticate/')
async def authenticateLoginDetails(email: str, password: str, db=Depends(get_db)):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    user = await db.fetchrow("""SELECT * FROM "User" WHERE email = $1""", email)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return {"user_id": user['user_id'], "is_admin": user['is_admin']}
    else:
        raise HTTPException(status_code=400, detail="Invalid email or password")