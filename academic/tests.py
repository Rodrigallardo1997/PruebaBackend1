"""
Pruebas Unitarias y de Integración - Sistema de Gestión Académica

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo ejecuta pruebas automáticas sobre:
1. Modelos de datos relacionales (Teacher, Course, Student, StudentCourse).
2. Endpoints de la API REST de Django REST Framework (DRF).
3. Vistas HTML y resolución de la ruta raíz '/' (eliminación de error 404).
"""

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Teacher, Course, Student, StudentCourse


class AcademicModelTests(TestCase):
    """Pruebas para verificar la integridad del modelo Entidad-Relación."""

    def setUp(self):
        self.teacher = Teacher.objects.create(first_name="Marcelo", last_name="Alvarado")
        self.course = Course.objects.create(name="Desarrollo Backend", teacher=self.teacher)
        self.student = Student.objects.create(first_name="Rodrigo", last_name="Gallardo")
        self.enrollment = StudentCourse.objects.create(student=self.student, course=self.course)

    def test_teacher_creation(self):
        """Verifica la creación y propiedades del docente."""
        self.assertEqual(self.teacher.full_name, "Marcelo Alvarado")
        self.assertEqual(str(self.teacher), f"{self.teacher.id} - Marcelo Alvarado")

    def test_course_creation(self):
        """Verifica la relación entre Curso y Docente (FK)."""
        self.assertEqual(self.course.teacher, self.teacher)
        self.assertEqual(self.course.name, "Desarrollo Backend")

    def test_student_creation(self):
        """Verifica la creación y propiedades del estudiante."""
        self.assertEqual(self.student.full_name, "Rodrigo Gallardo")

    def test_enrollment_creation(self):
        """Verifica la relación de inscripción (StudentCourse)."""
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)


class AcademicViewAndAPITests(TestCase):
    """Pruebas de endpoints REST y vistas HTML."""

    def setUp(self):
        self.client = Client()
        self.api_client = APIClient()
        self.teacher = Teacher.objects.create(first_name="Carolina", last_name="Herrera")
        self.course = Course.objects.create(name="Bases de Datos", teacher=self.teacher)
        self.student = Student.objects.create(first_name="Valentina", last_name="Morales")
        self.enrollment = StudentCourse.objects.create(student=self.student, course=self.course)

    def test_root_url_no_404(self):
        """Verifica que la ruta raíz '/' responda HTTP 200 (sin error 404)."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/index.html')

    def test_courses_view_html(self):
        """Verifica que la vista frontend /courses/ responda HTTP 200."""
        response = self.client.get('/courses/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/courses.html')

    def test_students_view_html(self):
        """Verifica que la vista frontend /students/ responda HTTP 200."""
        response = self.client.get('/students/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/students.html')

    def test_api_teachers_endpoint(self):
        """Verifica que /api/teachers/ retorne la lista en formato JSON."""
        response = self.api_client.get('/api/teachers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "Carolina")

    def test_api_courses_endpoint(self):
        """Verifica que /api/courses/ incluya el nombre del profesor asignado."""
        response = self.api_client.get('/api/courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['teacher_name'], "Carolina Herrera")

    def test_api_students_endpoint(self):
        """Verifica que /api/students/ retorne información del alumno e inscripciones."""
        response = self.api_client.get('/api/students/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "Valentina")

    def test_api_student_courses_endpoint(self):
        """Verifica que /api/student-courses/ retorne las inscripciones."""
        response = self.api_client.get('/api/student-courses/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
