from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from contextlib import asynccontextmanager
from src.utils.config_loader import CONFIG

# Создаём асинхронный движок:
engine = create_async_engine(CONFIG["DATABASE_URL"], future=True, echo=False)

SessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

@asynccontextmanager
async def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
