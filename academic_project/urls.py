"""
Configuración global de URLs del proyecto academic_project

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo delega las rutas principales a la aplicación 'academic'.
Incluye la ruta raíz '/', vistas de frontend, endpoints de la API y el panel de administración.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),

    # Delegación de todas las rutas de la app académica (Frontend y API REST)
    path('', include('academic.urls')),
]
