from app.db.base import Base
from app.db.session import engine
import app.models.auth
import app.models.analyze

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)