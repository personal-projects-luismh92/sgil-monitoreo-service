""" Archivo principal de la aplicación FastAPI """
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from common_for_services.database.connection import engine, Base, DB_NAME, DB_PASSWORD, DB_USER, DB_HOST_URL
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.sql import text
from app.routers import monitor, log


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("main_app")

admin_engine = create_async_engine(
    f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST_URL}/postgres",
    isolation_level="AUTOCOMMIT",
    echo=True
)

#  Crea la base de datos si no existe


async def create_database():
    """Check if the database exists; if not, create it."""
    async with admin_engine.connect() as conn:
        result = await conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}'"))
        exists = result.scalar()

        if not exists:
            await conn.execute(text(f'CREATE DATABASE "{DB_NAME}"'))
            logger.info(f"Database '{DB_NAME}' created successfully.")
        else:
            logger.info(f"Database '{DB_NAME}' already exists.")


# Crear todas las tablas en la base de datos (si no existen)
async def init_db():
    """ Crear todas las tablas en la base de datos (si no existen) """
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("Tablas creadas correctamente")

    except Exception as _:
        logger.critical(
            "La conexión a la base de datos en el servicio de monitoreo ha fallado al iniciar la aplicación")


# Instancia de la aplicación FastAPI
app = FastAPI(
    title="API de monitoreo de servicios",
    description="Una API para manejar el monitoreo de los servicios FastAPI y SQLAlchemy.",
    version="1.0.0"
)

# Configuración de CORS (Permitir acceso desde frontend)
app.add_middleware(
    CORSMiddleware,
    # Cambia esto por los dominios permitidos en producción
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar Routers
app.include_router(log.router, prefix="/logs", tags=["Logs"])
app.include_router(monitor.router, prefix="/monitor", tags=["Monitoring"])


# Health Check Endpoint
@app.get("/health")
def health_check():
    """Ruta principal de la API"""
    return {"status": "ok", "message": "API monitoreo funcionando correctamente"}


@app.on_event("startup")
async def on_startup():
    """ Crear la base de datos y las tablas al iniciar la aplicación """
    await create_database()
    await init_db()
