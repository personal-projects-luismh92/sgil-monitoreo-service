"""Routers para el manejo de logs."""
import logging
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



@router.post("")
async def store_log(log_data: LogCreate, db: AsyncSession = Depends(get_db)):
    """Recibe reportes de errores en queries de la base de datos."""
    return await LogEntryService.crear(db, log_data)
