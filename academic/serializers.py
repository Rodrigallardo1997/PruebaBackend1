"""
Serializadores de Django REST Framework (DRF)

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo define los serializadores que transforman las instancias de los modelos
y estructuras de datos en representaciones JSON nativas para la API REST.
"""

from rest_framework import serializers
from .models import Teacher, Course, Student, StudentCourse


class TeacherSerializer(serializers.ModelSerializer):
    """
    Serializador para la entidad Teacher (Docente).
    Mapea id, first_name, last_name y una propiedad calculada full_name.
    """
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'full_name']


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializador para la entidad Course (Asignatura).
    Mapea id, name y la clave foránea del docente.
    Incluye campos auxiliares como 'teacher_name' y 'teacher_detail' para que el frontend
    pueda mostrar directamente el nombre del profesor asignado.
    """
    # Permite obtener el nombre completo del docente asignado
    teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)
    # Objeto serializado completo del docente (anidado)
    teacher_detail = TeacherSerializer(source='teacher', read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'teacher', 'teacher_name', 'teacher_detail']


class StudentCourseSimpleSerializer(serializers.ModelSerializer):
    """
    Serializador ligero para representar inscripciones desde la perspectiva del estudiante.
    """
    course_name = serializers.CharField(source='course.name', read_only=True)
    teacher_name = serializers.CharField(source='course.teacher.full_name', read_only=True)

    class Meta:
        model = StudentCourse
        fields = ['id', 'course', 'course_name', 'teacher_name']


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializador para la entidad Student (Estudiante).
    Mapea id, first_name, last_name, full_name y la lista de cursos en los que está inscrito.
    """
    full_name = serializers.ReadOnlyField()
    # Lista de asignaturas inscritas por el alumno
    enrolled_courses = StudentCourseSimpleSerializer(source='enrollments', many=True, read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'full_name', 'enrolled_courses']


class StudentCourseSerializer(serializers.ModelSerializer):
    """
    Serializador para la entidad StudentCourse (Inscripción).
    Mapea las relaciones entre estudiante y asignatura con nombres legibles.
    """
    student_name = serializers.CharField(source='student.full_name', read_only=True)
    course_name = serializers.CharField(source='course.name', read_only=True)

    class Meta:
        model = StudentCourse
        fields = ['id', 'student', 'student_name', 'course', 'course_name']
