# backend/infrastructure/serializers.py
from rest_framework import serializers


class HOSRequestSerializer(serializers.Serializer):
    """Valida la entrada del usuario desde el frontend"""

    current_location = serializers.CharField(
        max_length=255, help_text="Ubicación actual del conductor (ej. 'Miami, FL')"
    )
    pickup_location = serializers.CharField(max_length=255, help_text="Punto de carga")
    dropoff_location = serializers.CharField(
        max_length=255, help_text="Punto de descarga"
    )
    current_cycle_used = serializers.FloatField(
        min_value=0.0,
        max_value=70.0,
        help_text="Horas ya consumidas en el ciclo de 70h",
    )


class TripEventSerializer(serializers.Serializer):
    """Transforma las entidades de dominio a JSON para el frontend"""

    status = serializers.SerializerMethodField()
    start_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    end_time = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    location = serializers.CharField()
    remarks = serializers.CharField()

    def get_status(self, obj):
        # Extrae el valor del Enum DutyStatus definido en el dominio
        return obj.status.value
