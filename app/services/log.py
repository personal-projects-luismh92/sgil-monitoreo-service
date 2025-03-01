""" Servicio para manejar los logs de la base de datos """
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.log import RepositorioLogEntry
from app.schemas.log import LogCreate


class LogEntryService:
    """ Servicio para manejar los logs de la base de datos """
    @staticmethod
    async def obtener_todos(db: AsyncSession, page: int, per_page: int):
        """ Obtiene todos los logs de forma asíncrona """
        return await RepositorioLogEntry.obtener_todos(db, page, per_page)

    @staticmethod
    async def obtener_por_id(db: AsyncSession, log_id: int):
        """ Obtiene un log por su ID de forma asíncrona """
        return await RepositorioLogEntry.obtener_por_id(db, log_id)

    @staticmethod
    async def crear(db: AsyncSession, log_data: LogCreate):
        """ Crea un nuevo log de forma asíncrona """
        return await RepositorioLogEntry.crear(db, log_data)

    @staticmethod
    async def actualizar(db: AsyncSession, log_id: int, log_data: LogCreate):
        """ Actualiza un log por su ID de forma asíncrona """
        return await RepositorioLogEntry.actualizar(db, log_id, log_data)

    @staticmethod
    async def eliminar(db: AsyncSession, log_id: int):
        """ Elimina un log por su ID de forma asíncrona """
        return await RepositorioLogEntry.eliminar(db, log_id)
