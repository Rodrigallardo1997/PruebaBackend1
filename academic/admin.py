"""
Configuración del Panel Administrativo de Django

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado
"""

from django.contrib import admin
from .models import Teacher, Course, Student, StudentCourse


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Configuración del modelo Teacher en el administrador."""
    list_display = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('id',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Configuración del modelo Course en el administrador."""
    list_display = ('id', 'name', 'teacher')
    list_filter = ('teacher',)
    search_fields = ('name', 'teacher__first_name', 'teacher__last_name')
    ordering = ('id',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Configuración del modelo Student en el administrador."""
    list_display = ('id', 'first_name', 'last_name')
    search_fields = ('first_name', 'last_name')
    ordering = ('id',)


@admin.register(StudentCourse)
class StudentCourseAdmin(admin.ModelAdmin):
    """Configuración de las inscripciones StudentCourse en el administrador."""
    list_display = ('id', 'student', 'course')
    list_filter = ('course', 'student')
    search_fields = ('student__first_name', 'student__last_name', 'course__name')
    ordering = ('id',)
