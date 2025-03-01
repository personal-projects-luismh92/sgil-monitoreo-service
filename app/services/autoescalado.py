from app.services.alerts import send_alert_email
from app.services.middleware import ANOMALY_DETECTION
import logging

logger = logging.getLogger("autoescalado_service")

# # Autoescalado basado en métricas de carga
def auto_scale():
    """ Escala automáticamente el número de instancias en función de la carga de solicitudes."""
    if ANOMALY_DETECTION._value.get() > 50:  # Ejemplo de umbral
        logger.info("Iniciando autoescalado: alta carga detectada")
        send_alert_email("Autoescalado Activado", "Se detectó una alta carga de solicitudes y se inició el autoescalado.")