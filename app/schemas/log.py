"""Schema de los logs"""
from pydantic import BaseModel
from typing import Optional


class LogBase(BaseModel):
    """Schema para el request de logs"""
    log: str
    service_name: str
    event: str
    error: str
    method: Optional[str] = None
    path: Optional[str] = None
    response_time: str
    timestamp: str


class LogCreate(LogBase):
    """ Esquema para la creación de una bodega """
    extra_data: Optional[dict] = None
