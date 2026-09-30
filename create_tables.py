import asyncio
from sqlalchemy import text
from app.database.session import engine
from app.database.base import Base
from app.models import *

async def create_tables():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS pulsedesk"))
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(create_tables())
