"""
Modelos de Datos - Sistema de Gestión Académica

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo define las entidades del dominio de acuerdo al modelo Entidad-Relación (ER):
1. Teacher (Docentes): id, first_name, last_name
2. Course (Asignaturas): id, name, teacher_id (FK a Teacher)
3. Student (Estudiantes): id, first_name, last_name
4. StudentCourse (Inscripciones): student_id (FK a Student), course_id (FK a Course)
"""

from django.db import models


class Teacher(models.Model):
    """
    Entidad Teacher (Docente)
    Representa a los profesores que imparten asignaturas en la institución.
    Campos:
        - id: Identificador único autoincremental (Clave Primaria).
        - first_name: Nombre del docente.
        - last_name: Apellido del docente.
        - degree: Grado académico (Choices: Licenciado, Magíster, Doctor).
    """
    DEGREE_CHOICES = [
        ('LIC', 'Licenciado(a)'),
        ('MAG', 'Magíster'),
        ('DOC', 'Doctor(a) / Ph.D.'),
    ]

    first_name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Nombre del docente"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Apellido",
        help_text="Apellido del docente"
    )
    degree = models.CharField(
        max_length=3,
        choices=DEGREE_CHOICES,
        default='MAG',
        verbose_name="Grado Académico",
        help_text="Nivel o grado académico del docente"
    )

    class Meta:
        db_table = 'teacher'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
        ordering = ['id']

    @property
    def full_name(self):
        """Retorna el nombre completo del docente."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.id} - {self.full_name} ({self.get_degree_display()})"


class Course(models.Model):
    """
    Entidad Course (Asignatura / Curso)
    Representa las materias académicas impartidas por un docente.
    Campos:
        - id: Identificador único autoincremental (Clave Primaria).
        - name: Nombre del curso / asignatura.
        - teacher: Clave foránea que referencia al Docente (teacher_id en el modelo ER).
        - modality: Modalidad de impartición (Choices: Presencial, Online, Híbrida).
    """
    MODALITY_CHOICES = [
        ('P', 'Presencial'),
        ('O', 'Online / Virtual'),
        ('H', 'Híbrida'),
    ]

    name = models.CharField(
        max_length=150,
        verbose_name="Nombre de la Asignatura",
        help_text="Nombre del curso o asignatura"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='courses',
        db_column='teacher_id',
        verbose_name="Docente Asignado",
        help_text="Profesor que imparte la asignatura"
    )
    modality = models.CharField(
        max_length=1,
        choices=MODALITY_CHOICES,
        default='P',
        verbose_name="Modalidad",
        help_text="Modalidad de impartición de la materia"
    )

    class Meta:
        db_table = 'course'
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['id']

    def __str__(self):
        return f"{self.name} [{self.get_modality_display()}] (Prof. {self.teacher.full_name if self.teacher else 'Sin asignar'})"


class Student(models.Model):
    """
    Entidad Student (Estudiante)
    Representa a los alumnos matriculados en la institución.
    Campos:
        - id: Identificador único autoincremental (Clave Primaria).
        - first_name: Nombre del estudiante.
        - last_name: Apellido del estudiante.
        - status: Estado de matrícula (Choices: Regular, Suspendido, Egresado).
        - gender: Género del estudiante (Choices: Masculino, Femenino, Otro).
    """
    STATUS_CHOICES = [
        ('ACT', 'Alumno Regular'),
        ('SUS', 'Suspendido'),
        ('EGR', 'Egresado'),
    ]
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    first_name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Nombre del estudiante"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Apellido",
        help_text="Apellido del estudiante"
    )
    status = models.CharField(
        max_length=3,
        choices=STATUS_CHOICES,
        default='ACT',
        verbose_name="Estado Académico",
        help_text="Estado actual de la matrícula"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        default='M',
        verbose_name="Género",
        help_text="Género del estudiante"
    )

    class Meta:
        db_table = 'student'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        ordering = ['id']

    @property
    def full_name(self):
        """Retorna el nombre completo del estudiante."""
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.id} - {self.full_name} ({self.get_status_display()})"


class StudentCourse(models.Model):
    """
    Entidad StudentCourse (Inscripción de Estudiante en Asignatura)
    Representa la relación muchos a muchos entre Estudiantes y Cursos.
    Campos:
        - student: Clave foránea al estudiante (student_id).
        - course: Clave foránea a la asignatura (course_id).
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='enrollments',
        db_column='student_id',
        verbose_name="Estudiante"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        db_column='course_id',
        verbose_name="Asignatura"
    )

    class Meta:
        db_table = 'student_course'
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
        # Garantiza que un estudiante no se inscriba dos veces en el mismo curso (clave primaria compuesta lógica)
        unique_together = ('student', 'course')
        ordering = ['id']

    def __str__(self):
        return f"Inscripción: {self.student.full_name} -> {self.course.name}"
