"""Módulo de configuración de la base de datos."""
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

DB_HOST_URL = os.environ.get("DB_HOST_URL", "127.0.0.1:5432")
DB_NAME = os.environ.get("DB_NAME", "sgil-monitor")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "123456")


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST_URL}/{DB_NAME}"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_db():
    """Crea una nueva sesión de base de datos para la solicitud."""
    async with async_session_maker() as session:
        yield session
