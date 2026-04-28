# backend/infrastructure/adapters.py
import requests
from typing import Tuple
from django.conf import settings
from backend.application.ports import IRoutingService


class OpenRouteServiceAdapter(IRoutingService):
    """
    Adaptador concreto para OpenRouteService.
    Implementa la interfaz definida en la capa de aplicación.
    """

    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-hgv"

    def __init__(self):
        # La API Key se lee de los settings de Django (que la toma del .env)
        self.api_key = getattr(settings, "ORS_API_KEY", "")

    def get_route_details(self, origin: str, destination: str) -> Tuple[float, float]:
        """
        Consulta a ORS para obtener distancia (m) y duración (s).
        Convierte los resultados a Millas y Horas para el HOSCalculator.
        """
        # Nota: En una versión de producción, aquí usarías un Geocodificador
        # para convertir nombres de ciudades a coordenadas [lon, lat].
        # Para la prueba, simularemos coordenadas o usaremos los nombres si la API lo permite.

        headers = {
            "Accept": "application/json, application/geo+json, charset=utf-8",
            "Authorization": self.api_key,
            "Content-Type": "application/json; charset=utf-8",
        }

        # En una implementación real de ORS, enviarías coordenadas.
        # Por ahora, simularemos la respuesta exitosa para integrar el flujo.
        # Si tienes coordenadas reales, el body sería: {"coordinates": [[lon1, lat1], [lon2, lat2]]}

        try:
            # Ejemplo de lógica de extracción (ajustar según respuesta real de ORS)
            # response = requests.post(self.BASE_URL, json=body, headers=headers)
            # data = response.json()
            # distance_meters = data['routes'][0]['summary']['distance']

            # Mock de seguridad si la petición falla o para desarrollo rápido:
            # Supongamos un viaje largo para probar las reglas HOS: 1500 miles / 25 hours
            distance_miles = 1500.0
            duration_hours = 25.0

            return distance_miles, duration_hours

        except Exception as e:
            print(f"Error connecting to ORS: {e}")
            return 0.0, 0.0
