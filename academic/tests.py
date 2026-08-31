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

    def test_teachers_view_html(self):
        """Verifica que la vista frontend /teachers/ responda HTTP 200."""
        response = self.client.get('/teachers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/teachers.html')

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

    def test_api_teachers_crud(self):
        """Prueba las operaciones CRUD completas en /api/teachers/."""
        # CREATE
        post_res = self.api_client.post('/api/teachers/', {'first_name': 'Gonzalo', 'last_name': 'Valenzuela'}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        teacher_id = post_res.data['id']

        # READ (DETAIL)
        get_res = self.api_client.get(f'/api/teachers/{teacher_id}/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['first_name'], 'Gonzalo')

        # UPDATE
        put_res = self.api_client.put(f'/api/teachers/{teacher_id}/', {'first_name': 'Gonzalo Andres', 'last_name': 'Valenzuela'}, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['first_name'], 'Gonzalo Andres')

        # DELETE
        del_res = self.api_client.delete(f'/api/teachers/{teacher_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_courses_crud(self):
        """Prueba las operaciones CRUD completas en /api/courses/."""
        # CREATE
        post_res = self.api_client.post('/api/courses/', {'name': 'Inteligencia Artificial', 'teacher': self.teacher.id}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        course_id = post_res.data['id']

        # READ (DETAIL)
        get_res = self.api_client.get(f'/api/courses/{course_id}/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['teacher_name'], 'Carolina Herrera')

        # UPDATE
        put_res = self.api_client.put(f'/api/courses/{course_id}/', {'name': 'IA Avanzada', 'teacher': self.teacher.id}, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['name'], 'IA Avanzada')

        # DELETE
        del_res = self.api_client.delete(f'/api/courses/{course_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_students_crud(self):
        """Prueba las operaciones CRUD completas en /api/students/."""
        # CREATE
        post_res = self.api_client.post('/api/students/', {'first_name': 'Camila', 'last_name': 'Rojas'}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        student_id = post_res.data['id']

        # READ
        get_res = self.api_client.get(f'/api/students/{student_id}/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['first_name'], 'Camila')

        # UPDATE
        put_res = self.api_client.put(f'/api/students/{student_id}/', {'first_name': 'Camila Paz', 'last_name': 'Rojas'}, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['first_name'], 'Camila Paz')

        # DELETE
        del_res = self.api_client.delete(f'/api/students/{student_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_student_courses_crud(self):
        """Prueba la inscripción y desinscripción de asignaturas."""
        # CREATE (Inscribir)
        new_student = Student.objects.create(first_name="Pedro", last_name="Pascal")
        post_res = self.api_client.post('/api/student-courses/', {'student': new_student.id, 'course': self.course.id}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        enrollment_id = post_res.data['id']

        # DELETE (Desinscribir)
        del_res = self.api_client.delete(f'/api/student-courses/{enrollment_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
