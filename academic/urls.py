"""
Configuración de URLs para la aplicación 'academic'

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo define:
1. Rutas Frontend:
   - '' (raíz): Vista de inicio/dashboard (elimina el error 404).
   - 'courses/': Vista de listado de cursos y profesores asignados.
   - 'students/': Vista de listado de estudiantes y asignaturas.
2. Rutas de la API REST mediante DefaultRouter de DRF:
   - 'api/teachers/': Endpoint para docentes.
   - 'api/courses/': Endpoint para asignaturas.
   - 'api/students/': Endpoint para estudiantes.
   - 'api/student-courses/': Endpoint para inscripciones.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    login_view,
    logout_view,
    index_view,
    demo_view,
    teachers_view,
    courses_view,
    students_view,
    TeacherViewSet,
    CourseViewSet,
    StudentViewSet,
    StudentCourseViewSet
)

# Inicialización del enrutador automático de DRF
router = DefaultRouter()
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'student-courses', StudentCourseViewSet, basename='student-course')

urlpatterns = [
    # Autenticación y Sesión de Usuarios
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Rutas Frontend Públicas (Sin CRUD)
    path('', index_view, name='home'),
    path('demo/', demo_view, name='demo'),

    # Rutas Frontend Protegidas (CRUD Completo para usuarios autenticados)
    path('teachers/', teachers_view, name='teachers'),
    path('courses/', courses_view, name='courses'),
    path('students/', students_view, name='students'),

    # Endpoints de Autenticación con Tokens JWT (Integración ej1)
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas API REST (Endpoints CRUD consumidos asíncronamente)
    path('api/', include(router.urls)),
]
