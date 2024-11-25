from sqlmodel import create_engine, text, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine

from src.config import CONFIG

engine = AsyncEngine(create_engine(CONFIG.DATABASE_URL, echo=True, future=True))


async def init_db():
    async with engine.begin() as conn:
        from src.db.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    async with Session() as session:
        yield session
