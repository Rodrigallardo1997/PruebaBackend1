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
        """Verifica la creación y propiedades del docente con choices."""
        self.assertEqual(self.teacher.full_name, "Marcelo Alvarado")
        self.assertEqual(str(self.teacher), f"{self.teacher.id} - Marcelo Alvarado (Magíster)")
        self.assertEqual(self.teacher.degree, "MAG")
        self.assertEqual(self.teacher.get_degree_display(), "Magíster")

        # Custom degree
        doc_teacher = Teacher.objects.create(first_name="Ada", last_name="Lovelace", degree="DOC")
        self.assertEqual(doc_teacher.degree, "DOC")
        self.assertEqual(doc_teacher.get_degree_display(), "Doctor(a) / Ph.D.")

    def test_course_creation(self):
        """Verifica la relación entre Curso y Docente (FK) y choices de modalidad."""
        self.assertEqual(self.course.teacher, self.teacher)
        self.assertEqual(self.course.name, "Desarrollo Backend")
        self.assertEqual(self.course.modality, "P")
        self.assertEqual(self.course.get_modality_display(), "Presencial")

        # Custom modality
        online_course = Course.objects.create(name="Redes", teacher=self.teacher, modality="O")
        self.assertEqual(online_course.modality, "O")
        self.assertEqual(online_course.get_modality_display(), "Online / Virtual")

    def test_student_creation(self):
        """Verifica la creación y propiedades del estudiante con choices de status y gender."""
        self.assertEqual(self.student.full_name, "Rodrigo Gallardo")
        self.assertEqual(self.student.status, "ACT")
        self.assertEqual(self.student.get_status_display(), "Alumno Regular")
        self.assertEqual(self.student.gender, "M")
        self.assertEqual(self.student.get_gender_display(), "Masculino")

        # Custom status & gender
        female_student = Student.objects.create(first_name="Maria", last_name="Perez", status="EGR", gender="F")
        self.assertEqual(female_student.status, "EGR")
        self.assertEqual(female_student.get_status_display(), "Egresado")
        self.assertEqual(female_student.gender, "F")
        self.assertEqual(female_student.get_gender_display(), "Femenino")

    def test_enrollment_creation(self):
        """Verifica la relación de inscripción (StudentCourse)."""
        self.assertEqual(self.enrollment.student, self.student)
        self.assertEqual(self.enrollment.course, self.course)


class AcademicViewAndAPITests(TestCase):
    """Pruebas de endpoints REST y vistas HTML."""

    def setUp(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        self.client = Client()
        self.api_client = APIClient()
        self.user = User.objects.create_user(username='admin_test', password='testpassword123')
        self.teacher = Teacher.objects.create(first_name="Carolina", last_name="Herrera")
        self.course = Course.objects.create(name="Bases de Datos", teacher=self.teacher)
        self.student = Student.objects.create(first_name="Valentina", last_name="Morales")
        self.enrollment = StudentCourse.objects.create(student=self.student, course=self.course)

    def test_root_url_public_landing_no_404(self):
        """Verifica que la vista pública raíz '/' responda HTTP 200 a visitantes sin login."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/index.html')

    def test_login_view_render_and_auth(self):
        """Verifica la vista de login y la autenticación de usuarios."""
        # Render formulario de login
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/login.html')

        # Login fallido (con cliente no autenticado)
        bad_response = self.client.post('/login/', {
            'username': 'admin_test',
            'password': 'wrongpassword'
        })
        self.assertEqual(bad_response.status_code, 200)
        self.assertContains(bad_response, 'incorrectos')

        # Login exitoso
        post_response = self.client.post('/login/', {
            'username': 'admin_test',
            'password': 'testpassword123'
        })
        self.assertEqual(post_response.status_code, 302)

    def test_unauthenticated_modules_redirect_to_login(self):
        """Verifica que visitantes sin autenticar sean redirigidos al login al intentar acceder a los módulos CRUD."""
        for path in ['/teachers/', '/courses/', '/students/']:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 302)
            self.assertIn('/login/', response.url)

    def test_authenticated_modules_access(self):
        """Verifica que usuarios autenticados puedan acceder a los módulos CRUD."""
        self.client.force_login(self.user)
        for path, template in [
            ('/teachers/', 'academic/teachers.html'),
            ('/courses/', 'academic/courses.html'),
            ('/students/', 'academic/students.html')
        ]:
            response = self.client.get(path)
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, template)

    def test_logout_view(self):
        """Verifica el cierre de sesión."""
        self.client.force_login(self.user)
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)

    def test_api_teachers_crud(self):
        """Prueba las operaciones CRUD completas en /api/teachers/ con choices."""
        # CREATE
        post_res = self.api_client.post('/api/teachers/', {'first_name': 'Gonzalo', 'last_name': 'Valenzuela', 'degree': 'DOC'}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        teacher_id = post_res.data['id']
        self.assertEqual(post_res.data['degree'], 'DOC')
        self.assertEqual(post_res.data['degree_display'], 'Doctor(a) / Ph.D.')

        # READ (DETAIL)
        get_res = self.api_client.get(f'/api/teachers/{teacher_id}/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['first_name'], 'Gonzalo')
        self.assertEqual(get_res.data['degree_display'], 'Doctor(a) / Ph.D.')

        # UPDATE
        put_res = self.api_client.put(f'/api/teachers/{teacher_id}/', {'first_name': 'Gonzalo Andres', 'last_name': 'Valenzuela', 'degree': 'MAG'}, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['first_name'], 'Gonzalo Andres')
        self.assertEqual(put_res.data['degree'], 'MAG')
        self.assertEqual(put_res.data['degree_display'], 'Magíster')

        # DELETE
        del_res = self.api_client.delete(f'/api/teachers/{teacher_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_courses_crud(self):
        """Prueba las operaciones CRUD completas en /api/courses/ con choices."""
        # CREATE
        post_res = self.api_client.post('/api/courses/', {'name': 'Inteligencia Artificial', 'teacher': self.teacher.id, 'modality': 'O'}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        course_id = post_res.data['id']
        self.assertEqual(post_res.data['modality'], 'O')
        self.assertEqual(post_res.data['modality_display'], 'Online / Virtual')

        # READ (DETAIL)
        get_res = self.api_client.get(f'/api/courses/{course_id}/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['teacher_name'], 'Carolina Herrera')
        self.assertEqual(get_res.data['modality_display'], 'Online / Virtual')

        # UPDATE
        put_res = self.api_client.put(f'/api/courses/{course_id}/', {'name': 'IA Avanzada', 'teacher': self.teacher.id, 'modality': 'H'}, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['name'], 'IA Avanzada')
        self.assertEqual(put_res.data['modality'], 'H')
        self.assertEqual(put_res.data['modality_display'], 'Híbrida')

        # DELETE
        del_res = self.api_client.delete(f'/api/courses/{course_id}/')
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_students_crud(self):
        """Prueba las operaciones CRUD completas en /api/students/ con choices."""
        # CREATE
        post_res = self.api_client.post('/api/students/', {'first_name': 'Camila', 'last_name': 'Rojas', 'status': 'ACT', 'gender': 'F'}, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        student_id = post_res.data['id']
        self.assertEqual(post_res.data['status'], 'ACT')
        self.assertEqual(post_res.data['status_display'], 'Alumno Regular')
        self.assertEqual(post_res.data['gender'], 'F')
        self.assertEqual(post_res.data['gender_display'], 'Femenino')

        # READ
        get_res = self.api_client.get(f'/api/students/{student_id}/')
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['first_name'], 'Camila')
        self.assertEqual(get_res.data['status_display'], 'Alumno Regular')
        self.assertEqual(get_res.data['gender_display'], 'Femenino')

        # UPDATE
        put_res = self.api_client.put(f'/api/students/{student_id}/', {'first_name': 'Camila Paz', 'last_name': 'Rojas', 'status': 'EGR', 'gender': 'F'}, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.assertEqual(put_res.data['first_name'], 'Camila Paz')
        self.assertEqual(put_res.data['status'], 'EGR')
        self.assertEqual(put_res.data['status_display'], 'Egresado')

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

    def test_jwt_token_obtain_and_refresh(self):
        """Prueba la generación y refresco de tokens JWT (SimpleJWT - ej1)."""
        from django.contrib.auth import get_user_model
        User = get_user_model()
        test_user = User.objects.create_user(username='testjwtuser', password='testpassword123')

        # Obtener Token
        token_res = self.api_client.post('/api/token/', {
            'username': 'testjwtuser',
            'password': 'testpassword123'
        }, format='json')
        self.assertEqual(token_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', token_res.data)
        self.assertIn('refresh', token_res.data)

        refresh_token = token_res.data['refresh']

        # Refrescar Token
        refresh_res = self.api_client.post('/api/token/refresh/', {
            'refresh': refresh_token
        }, format='json')
        self.assertEqual(refresh_res.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_res.data)

    def test_advanced_filtering_and_search(self):
        """Prueba el filtrado con DjangoFilterBackend y búsqueda (SearchFilter - ej1)."""
        # Filtrar por profesor ID
        filter_res = self.api_client.get(f'/api/courses/?teacher={self.teacher.id}')
        self.assertEqual(filter_res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(filter_res.data), 1)

        # Búsqueda textual con ?search=
        search_res = self.api_client.get('/api/courses/?search=Bases')
        self.assertEqual(search_res.status_code, status.HTTP_200_OK)
        self.assertEqual(search_res.data[0]['name'], "Bases de Datos")

    def test_choices_filtering(self):
        """Prueba el filtrado directo en los endpoints DRF usando campos de choices."""
        # Filtrar cursos por modalidad
        res_course = self.api_client.get('/api/courses/?modality=P')
        self.assertEqual(res_course.status_code, status.HTTP_200_OK)
        self.assertTrue(all(c['modality'] == 'P' for c in res_course.data))

        # Filtrar docentes por grado
        res_teacher = self.api_client.get('/api/teachers/?degree=LIC')
        self.assertEqual(res_teacher.status_code, status.HTTP_200_OK)
        self.assertTrue(all(t['degree'] == 'LIC' for t in res_teacher.data))

        # Filtrar estudiantes por status y gender
        res_student = self.api_client.get('/api/students/?status=ACT&gender=M')
        self.assertEqual(res_student.status_code, status.HTTP_200_OK)

    def test_demo_view_public_read_only(self):
        """Prueba que la vista de demostración /demo/ responda HTTP 200 a visitantes sin login."""
        response = self.client.get('/demo/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'academic/demo.html')

    def test_unregistered_url_redirects_to_home(self):
        """Verifica que cualquier URL mal escrita o no registrada redirija automáticamente a la página de inicio '/'."""
        for bad_path in ['/asdasd', '/asdasd/', '/pagina-inexistente', '/cualquier/ruta/invalida/']:
            response = self.client.get(bad_path)
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/')


