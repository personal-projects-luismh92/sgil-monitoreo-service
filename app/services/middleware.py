from fastapi import  Request, Response
import logging
import time
import datetime
import time
import os
import threading
import datetime
from collections import defaultdict
from prometheus_client import Counter, Histogram, Gauge
from sqlalchemy import text 
from app.services.alerts import send_alert_email
# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("middleware_service")


# # Métricas Prometheus
REQUEST_COUNT = Counter("api_requests_total",
                        "Total de solicitudes a la API", ["endpoint"])

ERROR_COUNT = Counter("api_errors_total",
                      "Total de errores detectados", ["error_type"])

REQUEST_LATENCY = Histogram("api_request_latency_seconds",
                            "Latencia de las solicitudes a la API", ["endpoint"])

ANOMALY_DETECTION = Gauge("api_anomalous_requests",
                          "Número de solicitudes anómalas detectadas")

# # Registro de patrones anómalos y bloqueo de IPs
anomaly_data = defaultdict(int)
blocked_ips = {}
LOCK = threading.Lock()
ANOMALY_THRESHOLD = 10  # Umbral de solicitudes anómalas por minuto
BLOCK_DURATION = 300  # Bloqueo de IPs en segundos (5 minutos)

# # Registro de eventos en la base de datos
def log_event(event_type, description, db):
    db.execute(text("""
        INSERT INTO event_log (event_type, description, timestamp) VALUES (:event_type, :description, NOW())
    """), {"event_type": event_type, "description": description})
    db.commit()

# Middleware para medir latencia de las solicitudes y detectar anomalías
# @app.middleware("http")
# async def detect_anomalies(request: Request, call_next):
#     client_ip = request.client.host
#     current_time = datetime.datetime.now().timestamp()

#     with LOCK:
#         # Verificar si la IP está bloqueada
#         if client_ip in blocked_ips and current_time < blocked_ips[client_ip]:
#             logger.warning(f"Blocked IP attempted access: {client_ip}")
#             return Response("Access denied", status_code=403)

#         start_time = time.time()
#         response = await call_next(request)
#         process_time = time.time() - start_time
#         REQUEST_LATENCY.labels(endpoint=request.url.path).observe(process_time)

#         # Detección de patrones anómalos por IP
#         anomaly_data[client_ip] += 1
#         if anomaly_data[client_ip] > ANOMALY_THRESHOLD:
#             ANOMALY_DETECTION.set(anomaly_data[client_ip])
#             logger.warning(f"Anomalous behavior detected from IP: {client_ip}, blocking for {BLOCK_DURATION} seconds")
#             send_alert_email("Anomalous Behavior Detected", f"Multiple suspicious requests detected from IP: {client_ip}. Blocking access for {BLOCK_DURATION} seconds.")
#             blocked_ips[client_ip] = current_time + BLOCK_DURATION
#             anomaly_data[client_ip] = 0  # Reiniciar contador tras bloqueo

#             with SessionLocal() as db:
#                 log_event("IP_BLOCKED", f"IP bloqueada: {client_ip}", db)