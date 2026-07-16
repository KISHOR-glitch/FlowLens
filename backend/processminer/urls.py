from django.urls import path
from .views import kpi_view

urlpatterns = [
    path("kpis/", kpi_view),
]