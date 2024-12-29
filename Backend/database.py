import asyncpg

DATABASE_URL = "postgresql://postgres:nourysushi@localhost:5432/Car-reantal"

# Dependency to get a database connection
async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


