from app.db.base import Base
from app.db.session import engine
import app.models.user
import app.models.analyze

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)