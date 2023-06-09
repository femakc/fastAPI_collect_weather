from typing import Generator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_URL

engine = create_async_engine(
    POSTGRES_URL,
    pool_size=200,
    max_overflow=250,
    future=True,
    echo=True,
    execution_options={"isolation_level": "READ COMMITTED"},
)

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)


async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
