from fastapi import HTTPException, APIRouter, Depends
from Backend.database import get_db
import bcrypt

router = APIRouter(
    prefix='/register',
    tags=['register']
)


@router.post('/create_user/')
async def create_customer(email: str, password: str, first_name: str, last_name: str, phone_number: str, city: str,
                          street: str, zip_code: str, db=Depends(get_db)):
    user = await db.fetchrow("""SELECT * FROM "User" WHERE email = $1""", email)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    await create_user(email, hashed_password_str, False, db=db)
    user = await db.fetchrow("""SELECT * FROM "User" WHERE email = $1""", email)
    user_id = user['user_id']
    try:
        await db.execute(
            """INSERT INTO Customer (first_name, last_name, phone_number, city, street, zip_code, user_id) VALUES ($1, $2, $3, $4, $5, $6, $7)""",
            first_name, last_name, phone_number, city, street, zip_code, user_id
        )
        return {"first_name": first_name, "last_name": last_name, "phone_number": phone_number, "city": city,
                "street": street, "zip_code": zip_code, "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=430, detail=str(e))


async def create_user(email: str, password: str, admin: bool = False, db=Depends(get_db)):
    try:
        await db.execute(
            """INSERT INTO "User" (email, password, is_admin) VALUES ($1, $2, $3)""",
            email, password, admin,
        )
        return {"email": email, "password": password, "admin": admin}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
