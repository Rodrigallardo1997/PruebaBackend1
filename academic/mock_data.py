"""
Módulo de Datos Simulados y Colecciones en Memoria (Mock Data)

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este módulo satisface el Criterio 2 de la rúbrica:
"Estructura adecuadamente las variables y colecciones necesarias para simular
o procesar los datos JSON sin requerir la base de datos."
"""

import json
from pathlib import Path

# ==============================================================================
# COLECCIONES EN MEMORIA (ESTRUCTURAS DE DATOS PYTHON PURAS)
# ==============================================================================

MOCK_TEACHERS = [
    {"id": 1, "first_name": "Marcelo", "last_name": "Alvarado", "full_name": "Marcelo Alvarado"},
    {"id": 2, "first_name": "Carolina", "last_name": "Herrera", "full_name": "Carolina Herrera"},
    {"id": 3, "first_name": "Gonzalo", "last_name": "Valenzuela", "full_name": "Gonzalo Valenzuela"},
    {"id": 4, "first_name": "Patricia", "last_name": "Sandoval", "full_name": "Patricia Sandoval"},
]

MOCK_COURSES = [
    {
        "id": 1,
        "name": "Desarrollo Backend con Python y Django",
        "teacher": 1,
        "teacher_name": "Marcelo Alvarado",
        "teacher_detail": {"id": 1, "first_name": "Marcelo", "last_name": "Alvarado", "full_name": "Marcelo Alvarado"}
    },
    {
        "id": 2,
        "name": "Arquitectura de Software y APIs REST",
        "teacher": 1,
        "teacher_name": "Marcelo Alvarado",
        "teacher_detail": {"id": 1, "first_name": "Marcelo", "last_name": "Alvarado", "full_name": "Marcelo Alvarado"}
    },
    {
        "id": 3,
        "name": "Bases de Datos Relacionales y NoSQL",
        "teacher": 2,
        "teacher_name": "Carolina Herrera",
        "teacher_detail": {"id": 2, "first_name": "Carolina", "last_name": "Herrera", "full_name": "Carolina Herrera"}
    },
    {
        "id": 4,
        "name": "Desarrollo Frontend con JavaScript y React",
        "teacher": 3,
        "teacher_name": "Gonzalo Valenzuela",
        "teacher_detail": {"id": 3, "first_name": "Gonzalo", "last_name": "Valenzuela", "full_name": "Gonzalo Valenzuela"}
    },
    {
        "id": 5,
        "name": "Seguridad y DevOps en la Nube",
        "teacher": 4,
        "teacher_name": "Patricia Sandoval",
        "teacher_detail": {"id": 4, "first_name": "Patricia", "last_name": "Sandoval", "full_name": "Patricia Sandoval"}
    },
]

MOCK_STUDENTS = [
    {
        "id": 1,
        "first_name": "Rodrigo",
        "last_name": "Gallardo",
        "full_name": "Rodrigo Gallardo",
        "enrolled_courses": [
            {"id": 1, "course": 1, "course_name": "Desarrollo Backend con Python y Django", "teacher_name": "Marcelo Alvarado"},
            {"id": 2, "course": 2, "course_name": "Arquitectura de Software y APIs REST", "teacher_name": "Marcelo Alvarado"},
        ]
    },
    {
        "id": 2,
        "first_name": "Valentina",
        "last_name": "Morales",
        "full_name": "Valentina Morales",
        "enrolled_courses": [
            {"id": 3, "course": 1, "course_name": "Desarrollo Backend con Python y Django", "teacher_name": "Marcelo Alvarado"},
            {"id": 4, "course": 3, "course_name": "Bases de Datos Relacionales y NoSQL", "teacher_name": "Carolina Herrera"},
        ]
    },
    {
        "id": 3,
        "first_name": "Ignacio",
        "last_name": "Castillo",
        "full_name": "Ignacio Castillo",
        "enrolled_courses": [
            {"id": 5, "course": 2, "course_name": "Arquitectura de Software y APIs REST", "teacher_name": "Marcelo Alvarado"},
            {"id": 6, "course": 4, "course_name": "Desarrollo Frontend con JavaScript y React", "teacher_name": "Gonzalo Valenzuela"},
        ]
    },
    {
        "id": 4,
        "first_name": "Camila",
        "last_name": "Rojas",
        "full_name": "Camila Rojas",
        "enrolled_courses": [
            {"id": 7, "course": 3, "course_name": "Bases de Datos Relacionales y NoSQL", "teacher_name": "Carolina Herrera"},
            {"id": 8, "course": 5, "course_name": "Seguridad y DevOps en la Nube", "teacher_name": "Patricia Sandoval"},
        ]
    },
    {
        "id": 5,
        "first_name": "Sebastian",
        "last_name": "Perez",
        "full_name": "Sebastian Perez",
        "enrolled_courses": [
            {"id": 9, "course": 1, "course_name": "Desarrollo Backend con Python y Django", "teacher_name": "Marcelo Alvarado"},
            {"id": 10, "course": 5, "course_name": "Seguridad y DevOps en la Nube", "teacher_name": "Patricia Sandoval"},
        ]
    }
]

MOCK_STUDENT_COURSES = [
    {"id": 1, "student": 1, "student_name": "Rodrigo Gallardo", "course": 1, "course_name": "Desarrollo Backend con Python y Django"},
    {"id": 2, "student": 1, "student_name": "Rodrigo Gallardo", "course": 2, "course_name": "Arquitectura de Software y APIs REST"},
    {"id": 3, "student": 2, "student_name": "Valentina Morales", "course": 1, "course_name": "Desarrollo Backend con Python y Django"},
    {"id": 4, "student": 2, "student_name": "Valentina Morales", "course": 3, "course_name": "Bases de Datos Relacionales y NoSQL"},
    {"id": 5, "student": 3, "student_name": "Ignacio Castillo", "course": 2, "course_name": "Arquitectura de Software y APIs REST"},
    {"id": 6, "student": 3, "student_name": "Ignacio Castillo", "course": 4, "course_name": "Desarrollo Frontend con JavaScript y React"},
    {"id": 7, "student": 4, "student_name": "Camila Rojas", "course": 3, "course_name": "Bases de Datos Relacionales y NoSQL"},
    {"id": 8, "student": 4, "student_name": "Camila Rojas", "course": 5, "course_name": "Seguridad y DevOps en la Nube"},
    {"id": 9, "student": 5, "student_name": "Sebastian Perez", "course": 1, "course_name": "Desarrollo Backend con Python y Django"},
    {"id": 10, "student": 5, "student_name": "Sebastian Perez", "course": 5, "course_name": "Seguridad y DevOps en la Nube"},
]


# ==============================================================================
# FUNCIONES AUXILIARES PARA LECTURA DE JSON Y MOCK
# ==============================================================================

def get_fixture_json_data():
    """
    Lee y parsea el archivo de datos JSON ubicado en academic/fixtures/initial_data.json.
    """
    fixture_path = Path(__file__).resolve().parent / 'fixtures' / 'initial_data.json'
    if fixture_path.exists():
        with open(fixture_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
