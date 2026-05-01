# backend/infrastructure/views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HOSRequestSerializer, TripEventSerializer
from .adapters import OpenRouteServiceAdapter
from backend.application.use_cases import GenerateTripLogsUseCase


# --- FUNCIONES AUXILIARES PARA EL MAPA VISUAL ---
def get_coordinates(city_name):
    url = (
        f"https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1"
    )
    headers = {"User-Agent": "SpotterELDSimulator/1.0"}
    try:
        response = requests.get(url, headers=headers).json()
        if response:
            return float(response[0]["lat"]), float(response[0]["lon"])
    except:
        pass
    return None, None


def get_route_path(lat1, lon1, lat2, lon2):
    url = f"https://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    try:
        response = requests.get(url, timeout=10).json()
        if response.get("code") == "Ok":
            geometry = response["routes"][0]["geometry"]["coordinates"]
            return [[coord[1], coord[0]] for coord in geometry]
    except Exception as e:
        print(f"OSRM error: {e}")
    return []


class CalculateELDView(APIView):
    """
    Endpoint principal para calcular la ruta y generar los logs HOS.
    """

    def post(self, request):
        # 1. Validar entrada
        serializer = HOSRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 2. Inyectar dependencias
        map_service = OpenRouteServiceAdapter()
        use_case = GenerateTripLogsUseCase(routing_service=map_service)

        # 3. Ejecutar lógica
        try:
            # Tu lógica de dominio intacta
            trip_events = use_case.execute(serializer.validated_data)
            output_serializer = TripEventSerializer(trip_events, many=True)

            # --- NUEVO: OBTENER DATOS VISUALES PARA EL MAPA ---
            origin_city = serializer.validated_data.get("current_location", "Miami, FL")
            destination_city = serializer.validated_data.get(
                "dropoff_location", "New York, NY"
            )

            lat1, lon1 = get_coordinates(origin_city)
            lat2, lon2 = get_coordinates(destination_city)

            # Fallback en caso de que la ciudad no exista
            if not lat1 or not lat2:
                lat1, lon1 = 25.7617, -80.1918
                lat2, lon2 = 40.7128, -74.0060

            route_path = get_route_path(lat1, lon1, lat2, lon2)

            # 4. Serializar salida combinada a JSON
            return Response(
                {
                    "events": output_serializer.data,
                    "map_data": {
                        "origin_coords": [lat1, lon1],
                        "destination_coords": [lat2, lon2],
                        "route_path": route_path,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
