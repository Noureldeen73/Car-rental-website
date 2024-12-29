from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncpg
from typing import Optional

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "postgresql://postgres:nourysushi@localhost:5432/Car-rental"

# Dependency to get a database connection
async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()

# Pydantic model for user
class User(BaseModel):
    id: Optional[int]
    email: str
    password: str
    admin: bool


# Create a new user
@app.post("/users/")
async def create_user(email: str, password: str, admin: bool, db=Depends(get_db)):
    try:
        await db.execute(
            """INSERT INTO "User" (email, password, is_admin) VALUES ($1, $2, $3)""",
            email, password, admin,
        )
        return {"email": email, "password": password, "admin": admin}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Get a user by ID
@app.get("/users/{id}")
async def get_user(id: int, db=Depends(get_db)):
    try:
        user = await db.fetchrow("""SELECT * FROM "User" WHERE user_id = $1""", id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return dict(user)  # Convert asyncpg record to dictionary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
