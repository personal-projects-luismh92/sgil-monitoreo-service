""" Modelo de la tabla log """
from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Integer, Numeric, UniqueConstraint, Index, JSON
)
from common_for_services.database.connection import Base


class LogEntry(Base):
    """ Modelo de la tabla log 
    Args:
        Base (SQLAlchemy): Clase base de SQLAlchemy

    Representa un registro de log en la base de datos.
        campos: 
            id: Identificador único del log
            log: Nivel de log (INFO, WARNING, ERROR, CRITICAL)
            service: Nombre del servicio que generó el log
            event: Evento que generó el log
            error: Error que generó el log
            method: Método HTTP que generó el log
            path: Ruta HTTP que generó el log
            response_time: Tiempo de respuesta del servicio que generó el log
            timestamp: Fecha y hora en que se generó el log
            extra_data: Datos adicionales del log
    """
    __tablename__ = "log"
    id = Column(Integer, primary_key=True, index=True)
    log = Column(String)
    service_name = Column(String, index=True)
    event = Column(String)
    error = Column(String)
    method = Column(String)
    path = Column(String)
    response_time = Column(String)
    timestamp = Column(String)
    extra_data = Column(JSON, nullable=True)
    __table_args__ = (
        Index("idx_service_event", "service_name", "event"),
        UniqueConstraint("id", name="uq_id"),
    )
