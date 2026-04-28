# backend/application/ports.py
from abc import ABC, abstractmethod
from typing import Tuple


class IRoutingService(ABC):
    """
    Puerto de salida (Outbound Port) para obtener datos de rutas.
    Cualquier API de mapas (Mapbox, ORS, Google Maps) debe implementar esta interfaz.
    """

    @abstractmethod
    def get_route_details(self, origin: str, destination: str) -> Tuple[float, float]:
        """
        Calcula la ruta entre dos puntos.

        Args:
            origin: Dirección o coordenadas de origen.
            destination: Dirección o coordenadas de destino.

        Returns:
            Tuple[float, float]: (distancia_en_millas, tiempo_estimado_en_horas)
        """
        pass
