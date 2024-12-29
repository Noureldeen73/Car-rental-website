import asyncpg
from fastapi import Depends

DATABASE_URL = "postgresql://postgres:eiad amel@localhost:5432/Car-rental"

# Dependency to get a database connection
async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


