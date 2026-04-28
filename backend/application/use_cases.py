# backend/application/use_cases.py
from datetime import datetime
from typing import List, Dict, Any
from backend.domain.models import TripEvent
from backend.domain.hos_calculator import HOSCalculator
from .ports import IRoutingService


class GenerateTripLogsUseCase:
    """
    Orquesta el flujo principal de la aplicación:
    Input -> Mapa -> HOSCalculator -> Output
    """

    def __init__(self, routing_service: IRoutingService):
        # Inyección de dependencias: El caso de uso no sabe qué API de mapas es,
        # solo sabe que cumple con IRoutingService.
        self.routing_service = routing_service

    def execute(self, request_data: Dict[str, Any]) -> List[TripEvent]:
        # 1. Extraer datos validados (asumimos que ya pasaron por el Serializer)
        current_location = request_data["current_location"]
        pickup_location = request_data["pickup_location"]
        dropoff_location = request_data["dropoff_location"]
        current_cycle_used = request_data["current_cycle_used"]

        # Para simplificar la prueba técnica, calculamos la ruta directa del pickup al dropoff.
        # (Si el conductor está muy lejos del pickup, se podría hacer una ruta en dos fases,
        # pero mantenemos el 'Assessment Assumption' simple primero).

        # 2. Consultar el servicio externo (El Adaptador)
        distance_miles, duration_hours = self.routing_service.get_route_details(
            origin=pickup_location, destination=dropoff_location
        )

        # Prevenir división por cero si los puntos son iguales
        if duration_hours <= 0:
            average_speed = 50.0  # Velocidad por defecto
        else:
            average_speed = distance_miles / duration_hours

        # 3. Iniciar el motor HOS (Dominio Puro)
        # Asumimos que el viaje empieza "ahora" para la simulación
        start_time = datetime.now()

        calculator = HOSCalculator(
            start_time=start_time,
            total_distance=distance_miles,
            average_speed=average_speed,
            current_cycle_used=current_cycle_used,
        )

        # 4. Generar y devolver los eventos
        events = calculator.generate_trip_events()

        # Opcional: Actualizar las ubicaciones de los eventos de inicio y fin con los nombres reales
        if events:
            events[0].location = pickup_location
            events[-1].location = dropoff_location

        return events
