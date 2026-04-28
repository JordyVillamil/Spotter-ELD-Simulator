# backend/infrastructure/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import HOSRequestSerializer, TripEventSerializer
from .adapters import OpenRouteServiceAdapter
from backend.application.use_cases import GenerateTripLogsUseCase


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
        # Creamos el adaptador y se lo pasamos al caso de uso.
        map_service = OpenRouteServiceAdapter()
        use_case = GenerateTripLogsUseCase(routing_service=map_service)

        # 3. Ejecutar lógica
        try:
            trip_events = use_case.execute(serializer.validated_data)

            # 4. Serializar salida de dominio a JSON
            output_serializer = TripEventSerializer(trip_events, many=True)
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
