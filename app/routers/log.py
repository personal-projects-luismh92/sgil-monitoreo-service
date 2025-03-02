"""Routers para el manejo de logs."""
import logging
import psutil
import asyncio
from fastapi import APIRouter, Depends
from common_for_services.database.connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.log import LogEntryService
from app.schemas.log import LogCreate

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("logs_routers")

router = APIRouter()


@router.get("/health")
async def health_check():
    """Verifica que la API esté funcionando correctamente"""
    try:

        # Call the function
        cpu_usage = await asyncio.to_thread(psutil.cpu_percent)
        # Wrap in lambda
        memory_usage = await asyncio.to_thread(lambda: psutil.virtual_memory().percent)

        return {
            "status": "ok",
            "message": "API logs funcionando correctamente",
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage
        }

    except Exception as e:
        return {"status": "error",
                "message": "Error al verificar la salud de la API",
                "details": str(e)}


@router.post("")
async def store_log(log_data: LogCreate, db: AsyncSession = Depends(get_db)):
    """Recibe reportes de errores en queries de la base de datos."""
    return await LogEntryService.crear(db, log_data)
