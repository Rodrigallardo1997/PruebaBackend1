"""
Vistas de la Aplicación - Sistema de Gestión Académica

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo contiene:
1. Vistas Frontend (HTML Renderers):
   - index_view: Maneja la ruta raíz "/" para eliminar el error 404 y presenta el dashboard.
   - courses_view: Renderiza la plantilla 'courses.html' (enmascara /api/courses/).
   - students_view: Renderiza la plantilla 'students.html' (enmascara /api/students/).
2. Vistas API REST (Django REST Framework):
   - TeacherViewSet / TeacherListAPIView: Expone docentes (/api/teachers/).
   - CourseViewSet / CourseListAPIView: Expone cursos con profesor asignado (/api/courses/).
   - StudentViewSet / StudentListAPIView: Expone estudiantes e inscripciones (/api/students/).
   - StudentCourseViewSet: Expone inscripciones (/api/student-courses/).
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend

from .models import Teacher, Course, Student, StudentCourse
from .serializers import (
    TeacherSerializer,
    CourseSerializer,
    StudentSerializer,
    StudentCourseSerializer
)
from .mock_data import (
    MOCK_TEACHERS,
    MOCK_COURSES,
    MOCK_STUDENTS,
    MOCK_STUDENT_COURSES
)


# ==============================================================================
# VISTAS DE AUTENTICACIÓN Y CONTROL DE ACCESO
# ==============================================================================

def login_view(request):
    """
    Vista de inicio de sesión con formulario Bootstrap.
    Permite autenticar al usuario y redirigirlo al módulo que intentaba acceder.
    """
    if request.user.is_authenticated:
        return redirect('home')

    error_message = None
    next_url = request.GET.get('next', 'home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        next_url = request.POST.get('next', 'home')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url if next_url else 'home')
        else:
            error_message = "Usuario o contraseña incorrectos. Por favor intenta nuevamente."

    context = {
        'page_title': 'Iniciar Sesión - Plataforma de Gestión Académica',
        'error_message': error_message,
        'next': next_url,
    }
    return render(request, 'academic/login.html', context)


def logout_view(request):
    """
    Cierra la sesión del usuario actual y lo redirige a la vista pública.
    """
    logout(request)
    return redirect('home')


# ==============================================================================
# VISTAS FRONTEND (RENDERIZADO DE PLANTILLAS HTML - "ENMASCARAMIENTO")
# ==============================================================================

def index_view(request):
    """
    Vista pública principal para la ruta raíz ("/").
    Disponible de forma gratuita/abierta para que cualquier visitante vea la
    arquitectura, estadísticas y qué hace la plataforma académica.
    """
    context = {
        'page_title': 'Inicio - Plataforma de Gestión Académica',
        'active_tab': 'home'
    }
    return render(request, 'academic/index.html', context)


@login_required(login_url='login')
def courses_view(request):
    """
    Vista frontend para la gestión de Cursos (Requiere Autenticación).
    Renderiza 'courses.html' y permite interactuar con el CRUD vía fetch().
    """
    context = {
        'page_title': 'Gestión de Asignaturas y Cursos',
        'active_tab': 'courses'
    }
    return render(request, 'academic/courses.html', context)


@login_required(login_url='login')
def students_view(request):
    """
    Vista frontend para la gestión de Estudiantes (Requiere Autenticación).
    Renderiza 'students.html' y permite interactuar con el CRUD vía fetch().
    """
    context = {
        'page_title': 'Gestión de Estudiantes Matriculados',
        'active_tab': 'students'
    }
    return render(request, 'academic/students.html', context)


@login_required(login_url='login')
def teachers_view(request):
    """
    Vista frontend para la gestión de Docentes (Requiere Autenticación).
    Renderiza 'teachers.html' y permite interactuar con el CRUD vía fetch().
    """
    context = {
        'page_title': 'Gestión de Docentes y Profesores',
        'active_tab': 'teachers'
    }
    return render(request, 'academic/teachers.html', context)


def demo_view(request):
    """
    Vista pública de demostración del sistema (Modo Solo Lectura, sin CRUD).
    Permite a visitantes ver cómo se visualizan las tablas y datos del sistema
    (Docentes, Cursos y Estudiantes) consumidos asíncronamente mediante Fetch API
    sin ofrecer ninguna opción de creación, edición o eliminación.
    """
    context = {
        'page_title': 'Demostración del Sistema (Solo Lectura)',
        'active_tab': 'demo'
    }
    return render(request, 'academic/demo.html', context)


# ==============================================================================
# VIEWSETS / ENDPOINTS REST CON DJANGO REST FRAMEWORK (DRF)
# Integración con django_filters, SearchFilter y OrderingFilter (ej1)
# ==============================================================================

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Teacher.
    Proporciona operaciones CRUD estándar sobre /api/teachers/.
    Soporta filtros por first_name, last_name, degree (Choices) y búsqueda textual.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name', 'degree']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name', 'degree']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists() or self.get_queryset().exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria si la BD está completamente vacía
        return Response(MOCK_TEACHERS, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Course.
    Proporciona endpoints para listar y detallar cursos en /api/courses/.
    Soporta filtros por teacher (ID), name, modality (Choices) y búsqueda.
    """
    queryset = Course.objects.select_related('teacher').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['teacher', 'name', 'modality']
    search_fields = ['name', 'teacher__first_name', 'teacher__last_name']
    ordering_fields = ['id', 'name', 'modality', 'teacher']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists() or self.get_queryset().exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_COURSES, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Student.
    Proporciona endpoints sobre /api/students/.
    Soporta filtros por first_name, last_name, status (Choices), gender (Choices) y búsqueda.
    """
    queryset = Student.objects.prefetch_related('enrollments__course__teacher').all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name', 'status', 'gender']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name', 'status', 'gender']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists() or self.get_queryset().exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_STUDENTS, status=status.HTTP_200_OK)


class StudentCourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad StudentCourse.
    Proporciona endpoints sobre /api/student-courses/.
    Soporta filtros por student (ID) y course (ID).
    """
    queryset = StudentCourse.objects.select_related('student', 'course').all()
    serializer_class = StudentCourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'course']
    ordering_fields = ['id', 'student', 'course']

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if queryset.exists() or self.get_queryset().exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_STUDENT_COURSES, status=status.HTTP_200_OK)


# ==============================================================================
# MANEJADORES DE ERRORES HTTP PERSONALIZADOS (404 / 500)
# ==============================================================================

def custom_404_view(request, exception=None):
    """
    Manejador para errores 404 (Página no encontrada).
    Retorna la plantilla 404.html con código de estado HTTP 404.
    """
    return render(request, '404.html', status=404)


def custom_500_view(request):
    """
    Manejador para errores 500 (Error interno del servidor).
    Retorna la plantilla 500.html con código de estado HTTP 500.
    """
    return render(request, '500.html', status=500)

