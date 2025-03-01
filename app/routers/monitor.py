""" Módulo de monitoreo de la API """
import logging
from app.services import api_health
from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import text
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
# Configurar logging estructurado
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("monitoring_routers")

router = APIRouter()


@router.get("/check-api-health",
            summary="Check API and Database Health",
            tags=["Monitoring"])
async def check_api_health():
    """
        Consulta el estado de todas las APIs y su conexión con la base de datos.
    """
    try:
        health_status = await api_health.check_api_health()
        logger.info("el chequeo de salud de las APIs se completó correctamente")
        return {"status": "success", "message": "Chequeo de salud de la API completado correctamente", "data": health_status}
    except Exception as e:
        logger.error(f"Error durante el chequeo de salud de la API: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Error al chequear la salud de la API")


@router.post("/report-anomaly")
def generate_report(db):
    """ Genera un reporte de eventos en la base de datos y lo envía por email."""
    print("Generando reporte de eventos... monitorig_service")
    result = db.execute(
        text("SELECT event_type, COUNT(*) FROM event_log GROUP BY event_type"))
    report = "Reporte de eventos:\n" + \
        "\n".join([f"{row[0]}: {row[1]} ocurrencias" for row in result])
    # alerts.send_alert_email("Reporte de Monitoreo", report)
    logger.info("Reporte de monitoreo enviado")


@router.get("/metrics")
async def metrics():
    """ Endpoint para exponer métricas Prometheus
    """
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
