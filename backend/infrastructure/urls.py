# backend/infrastructure/urls.py
from django.urls import path
from .views import CalculateELDView

urlpatterns = [
    # Esto manejará la petición a /api/v1/calculate-eld/
    path("calculate-eld/", CalculateELDView.as_view(), name="calculate-eld"),
]
