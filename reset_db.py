import asyncio
from sqlalchemy import text
from app.database.session import engine

async def reset():
    async with engine.begin() as conn:
        await conn.execute(text("DROP SCHEMA IF EXISTS pulsedesk CASCADE"))
        try:
            await conn.execute(text("DROP TYPE IF EXISTS ticketpriority CASCADE"))
            await conn.execute(text("DROP TYPE IF EXISTS ticketstatus CASCADE"))
        except Exception:
            pass

asyncio.run(reset())
