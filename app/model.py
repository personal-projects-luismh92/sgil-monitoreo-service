# import pandas as pd
# import numpy as np
# from sklearn.ensemble import IsolationForest

# # Datos históricos de tráfico (Ejemplo: IP, número de solicitudes)
# traffic_data = pd.DataFrame(columns=["requests_per_minute"])

# # Entrenar modelo de Isolation Forest
# def train_anomaly_model():
#     global model
#     if len(traffic_data) > 10:  # Necesitamos suficiente data
#         model = IsolationForest(contamination=0.05)
#         model.fit(traffic_data)
# train_anomaly_model()

# @app.middleware("http")
# async def detect_anomalies(request: Request, call_next):
#     client_ip = request.client.host
#     current_time = datetime.datetime.now().timestamp()

#     # Registrar número de solicitudes por minuto
#     with LOCK:
#         anomaly_data[client_ip] += 1
#         traffic_data.loc[len(traffic_data)] = [anomaly_data[client_ip]]
    
#     # Detectar anomalías usando Machine Learning
#     if len(traffic_data) > 10:
#         prediction = model.predict(np.array(traffic_data.tail(1)))
#         if prediction[0] == -1:  # Se detecta anomalía
#             logger.warning(f"🚨 Anomalous behavior detected from IP: {client_ip}")
#             send_alert_email("Alerta de Anomalía", f"Tráfico sospechoso detectado desde IP: {client_ip}")

#     response = await call_next(request)
#     return response


# from fastapi import FastAPI, Depends, Request
# import httpx
# import logging
# import json


# import time
# import os
# import threading
# import datetime
# from collections import defaultdict
# from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# app = FastAPI()

# # Configurar logging estructurado
# logging.basicConfig(level=logging.INFO, format='%(message)s')
# logger = logging.getLogger("monitoring_service")



# # Contador de errores en queries
# query_failure_counter = Counter(
#     "db_query_failures", "Número de errores en queries de la base de datos")
# # Configuración de logging
# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)

