""" Módulo que contiene la clase RepositorioLogEntry """
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import Query
from app.models.log import LogEntry
from app.schemas.log import LogCreate


class RepositorioLogEntry:
    """Clase que maneja las operaciones de la tabla log en la base de datos"""
    @staticmethod
    async def obtener_todos(db: AsyncSession,
                            page: Optional[int] = Query(
                                None, alias="page", ge=0),
                            size: Optional[int] = Query(None, alias="size", ge=1, le=100)):
        """Obtiene todos los loges de forma asíncrona"""

        # Count total records before pagination
        # Count the rows by the 'id' column
        count_query = select(func.count(LogEntry.id))
        result = await db.execute(count_query)
        total_rows = result.scalar()  # Get the count of rows

        # Base query for getting rows
        query = select(LogEntry)

        # Apply pagination if both page and size are provided
        if page is not None and size is not None:
            query = query.offset(page * size).limit(size)
            total_pages = (total_rows + size - 1) // size  # Ceiling division
        else:
            total_pages = None  # No pagination

        # Execute the query to fetch the results
        result = await db.execute(query)
        data = result.scalars().all()  # Get the results as a list

        # Prepare the response
        response = {
            "data": data,
            "totalRows": total_rows,
            "totalPages": total_pages
        }

        if total_pages is None:
            del response["totalPages"]

        return response

    @staticmethod
    async def obtener_por_id(db: AsyncSession, log_id: int):
        """Obtiene un log por su ID de forma asíncrona"""
        result = await db.execute(select(LogEntry).filter_by(id=log_id))
        return result.scalars().first()

    @staticmethod
    async def crear(db: AsyncSession, log_data: LogCreate):
        """Crea un nuevo log de forma asíncrona""" 
        nuevo_log = LogEntry(**log_data.model_dump())

        db.add(nuevo_log)
        await db.flush()
        await db.commit()
        await db.refresh(nuevo_log)

        return nuevo_log

    @staticmethod
    async def actualizar(db: AsyncSession, log_id: int, log_data: LogCreate):
        """Actualiza un log existente de forma asíncrona"""
        result = await db.execute(select(LogEntry).filter_by(id=log_id))
        log = result.scalars().first()
        if log:
            for key, value in log_data.model_dump().items():
                setattr(log, key, value)
            await db.commit()
            await db.refresh(log)
        return log

    @staticmethod
    async def eliminar(db: AsyncSession, log_id: int):
        """Elimina un log por su ID de forma asíncrona"""
        result = await db.execute(select(LogEntry).filter_by(id=log_id))
        log = result.scalars().first()
        if log:
            await db.delete(log)
            await db.commit()
            return True
        return False
