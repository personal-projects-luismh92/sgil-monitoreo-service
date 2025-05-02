""" Módulo para monitorear el estado de las APIs. """
import logging
import json
import os
import httpx

# Configurar logging estructurado
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("monitoring_service")

# Definir APIs a monitorear
BODEGAS_URL = os.getenv(
    "BODEGAS_URL", "http://sgil-inventario-service:80/inventario/bodegas/health")
USUARIOS_URL = os.getenv(
    "USUARIOS_URL", "http://sgil-usuarios-service:80/usuarios/health")
PEDIDOS_URL = os.getenv(
    "PEDIDOS_URL", "http://sgil-pedidos-service:80/pedidos/health")
VENDEDORES_URL = os.getenv(
    "PEDIDOS_URL", "http://sgil-vendedores-service:80/vendedores/health")
# Definir las URLs de las APIs a monitorear
API_SERVICES = [
    {"name": "Usuarios", "url": USUARIOS_URL},
    {"name": "Pedidos", "url": PEDIDOS_URL},
    {"name": "Vendedores", "url": VENDEDORES_URL},
    {"name": "Bodegas", "url": BODEGAS_URL},
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
