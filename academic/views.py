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

from django.shortcuts import render
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
# VISTAS FRONTEND (RENDERIZADO DE PLANTILLAS HTML - "ENMASCARAMIENTO")
# ==============================================================================

def index_view(request):
    """
    Vista principal para la ruta raíz ("/").
    Elimina el error 404 cuando se ingresa a la raíz del servidor.
    Renderiza un panel de bienvenida con accesos rápidos a Cursos, Estudiantes y Endpoints API.
    """
    context = {
        'page_title': 'Inicio - Plataforma de Gestión Académica',
        'active_tab': 'home'
    }
    return render(request, 'academic/index.html', context)


def courses_view(request):
    """
    Vista frontend para el listado de Cursos.
    Renderiza la plantilla HTML 'courses.html', la cual consume asíncronamente
    los datos desde '/api/courses/' mediante JavaScript fetch().
    """
    context = {
        'page_title': 'Gestión de Asignaturas y Cursos',
        'active_tab': 'courses'
    }
    return render(request, 'academic/courses.html', context)


def students_view(request):
    """
    Vista frontend para el listado y gestión CRUD de Estudiantes.
    Renderiza la plantilla HTML 'students.html', la cual consume asíncronamente
    los datos desde '/api/students/' mediante JavaScript fetch().
    """
    context = {
        'page_title': 'Gestión de Estudiantes Matriculados',
        'active_tab': 'students'
    }
    return render(request, 'academic/students.html', context)


def teachers_view(request):
    """
    Vista frontend para el listado y gestión CRUD de Docentes.
    Renderiza la plantilla HTML 'teachers.html', la cual consume asíncronamente
    los datos desde '/api/teachers/' mediante JavaScript fetch().
    """
    context = {
        'page_title': 'Gestión de Docentes y Profesores',
        'active_tab': 'teachers'
    }
    return render(request, 'academic/teachers.html', context)


def docs_view(request):
    """
    Vista frontend para la Documentación Interactiva de la API (Swagger UI).
    Renderiza 'docs.html' conectado con el esquema OpenAPI generado automáticamente por DRF.
    """
    context = {
        'page_title': 'Documentación de la API - OpenAPI / Swagger',
        'active_tab': 'docs'
    }
    return render(request, 'academic/docs.html', context)


# ==============================================================================
# VIEWSETS / ENDPOINTS REST CON DJANGO REST FRAMEWORK (DRF)
# Integración con django_filters, SearchFilter y OrderingFilter (ej1)
# ==============================================================================

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Teacher.
    Proporciona operaciones CRUD estándar sobre /api/teachers/.
    Soporta filtros por first_name, last_name y búsqueda textual.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name']

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
    Soporta filtros por teacher (ID), name, búsqueda por docente y ordenamiento.
    """
    queryset = Course.objects.select_related('teacher').all()
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['teacher', 'name']
    search_fields = ['name', 'teacher__first_name', 'teacher__last_name']
    ordering_fields = ['id', 'name', 'teacher']

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
    Soporta filtros por first_name, last_name, búsqueda y ordenamiento.
    """
    queryset = Student.objects.prefetch_related('enrollments__course__teacher').all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['id', 'first_name', 'last_name']

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
