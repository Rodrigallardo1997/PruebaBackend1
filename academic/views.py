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
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    Vista frontend para el listado de Estudiantes.
    Renderiza la plantilla HTML 'students.html', la cual consume asíncronamente
    los datos desde '/api/students/' mediante JavaScript fetch().
    """
    context = {
        'page_title': 'Gestión de Estudiantes Matriculados',
        'active_tab': 'students'
    }
    return render(request, 'academic/students.html', context)


# ==============================================================================
# VIEWSETS / ENDPOINTS REST CON DJANGO REST FRAMEWORK (DRF)
# ==============================================================================

class TeacherViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Teacher.
    Proporciona operaciones CRUD estándar sobre /api/teachers/.
    Si la base de datos no tiene registros, provee fallback a colecciones en memoria.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_TEACHERS, status=status.HTTP_200_OK)


class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Course.
    Proporciona endpoints para listar y detallar cursos en /api/courses/.
    Optimiza consultas con select_related('teacher') para incluir información del docente.
    """
    queryset = Course.objects.select_related('teacher').all()
    serializer_class = CourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_COURSES, status=status.HTTP_200_OK)


class StudentViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad Student.
    Proporciona endpoints sobre /api/students/.
    Incluye prefetch_related para traer las inscripciones y asignaturas de cada estudiante.
    """
    queryset = Student.objects.prefetch_related('enrollments__course__teacher').all()
    serializer_class = StudentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_STUDENTS, status=status.HTTP_200_OK)


class StudentCourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet DRF para la entidad StudentCourse.
    Proporciona endpoints sobre /api/student-courses/.
    """
    queryset = StudentCourse.objects.select_related('student', 'course').all()
    serializer_class = StudentCourseSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        # Fallback a datos simulados en memoria
        return Response(MOCK_STUDENT_COURSES, status=status.HTTP_200_OK)
