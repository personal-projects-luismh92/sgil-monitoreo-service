""" Módulo para monitorear el estado de las APIs. """
import httpx
import logging
import json
import os

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("monitoring_service")

# Definir APIs a monitorear
API_SERVICES = [
    {"name": "Usuarios", "url": "http://usuarios-service/health"},
    {"name": "Pedidos", "url": "http://pedidos-service/health"},
    {"name": "Pagos", "url": "http://pagos-service/health"},
    {"name": "Bodegas", "url": os.getenv("BODEGAS_URL", "http://localhost:8001/inventario/bodegas/health")},
]

async def check_api_health():
    """Consulta el estado de cada API y su base de datos."""
    results = []
    async with httpx.AsyncClient() as client:
        for service in API_SERVICES:
            try:
                response = await client.get(service["url"], timeout=3.0)
                results.append(
                    {"service": service["name"], "status": response.json()})
            
            except Exception as e:
                results.append(
                    {"service": service["name"],
                     "status": "DOWN",
                     "error": str(e)})
                
                logger.error(json.dumps(
                    {"event": "api_down", 
                     "service": service["name"], 
                     "error": str(e)}))
                
                # send_alert_email(f"Alerta: {service['name']} está caída",
                #                  f"Error: {str(e)}")
    return results
