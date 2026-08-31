# Registro de Prompts de Inteligencia Artificial (Entregable IA)

**Evaluación N°1: Desarrollo Backend con Django & DRF**  
**Asignatura:** Desarrollo Backend  
**Docente:** Marcelo Alvarado  
**Estudiante:** Rodrigo Gallardo  
**Herramienta de IA:** Google Gemini / Claude  

---

## Índice de Prompts
1. [Prompt 1: Diseño y Estructuración de Modelos ER y Serializadores DRF](#prompt-1-diseño-y-estructuración-de-modelos-er-y-serializadores-drf)
2. [Prompt 2: Generación del Conjunto de Datos Ficticios en Formato JSON](#prompt-2-generación-del-conjunto-de-datos-ficticios-en-formato-json)
3. [Prompt 3: Maquetación y Diseño de Plantillas HTML con Bootstrap 5](#prompt-3-maquetación-y-diseño-de-plantillas-html-con-bootstrap-5)
4. [Prompt 4: Implementación de Código Asíncrono con JavaScript Fetch API](#prompt-4-implementación-de-código-asíncrono-con-javascript-fetch-api)
5. [Prompt 5: Resolución de la Ruta Raíz '/' y Eliminación del Error 404](#prompt-5-resolución-de-la-ruta-raíz--y-eliminación-del-error-404)

---

## Prompt 1: Diseño y Estructuración de Modelos ER y Serializadores DRF

### 📥 Prompt Enviado:
```text
Actúa como un desarrollador backend senior en Python y Django REST Framework.
Tengo el siguiente esquema Entidad-Relación (ER) para un sistema de gestión académica:
- Teacher (id PK, first_name varchar, last_name varchar)
- Course (id PK, name varchar, teacher_id FK a Teacher)
- Student (id PK, first_name varchar, last_name varchar)
- StudentCourse (student_id PK/FK a Student, course_id PK/FK a Course)

Requiero:
1. El código de models.py para la app 'academic' con relaciones ForeignKey, campos informativos, verbose_name, métodos __str__ y comentarios detallados.
2. Los serializadores en serializers.py usando ModelSerializer de DRF, asegurando que CourseSerializer devuelva el nombre legible del profesor y StudentSerializer incluya sus cursos matriculados.
```

### 📤 Respuesta Generada por la IA:
```python
# models.py
from django.db import models

class Teacher(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    
    class Meta:
        db_table = 'teacher'
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.id} - {self.full_name}"

class Course(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre de la Asignatura")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses', db_column='teacher_id')
    
    class Meta:
        db_table = 'course'
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        
    def __str__(self):
        return self.name

class Student(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombre")
    last_name = models.CharField(max_length=100, verbose_name="Apellido")
    
    class Meta:
        db_table = 'student'
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'
        
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return f"{self.id} - {self.full_name}"

class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments', db_column='student_id')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments', db_column='course_id')
    
    class Meta:
        db_table = 'student_course'
        unique_together = ('student', 'course')
        verbose_name = 'Inscripción'
        verbose_name_plural = 'Inscripciones'
```

---

## Prompt 2: Generación del Conjunto de Datos Ficticios en Formato JSON

### 📥 Prompt Enviado:
```text
Genera un conjunto de datos ficticios en formato JSON compatible con fixtures de Django (manage.py loaddata) para precargar la base de datos del sistema académico.
Debe incluir:
- Al menos 4 profesores (Teacher)
- Al menos 5 cursos universitarios reales (Course) asignados a dichos profesores
- Al menos 5 estudiantes (Student), incluyendo al estudiante 'Rodrigo Gallardo'
- Múltiples inscripciones (StudentCourse) para simular relaciones 1:N y N:M
```

### 📤 Respuesta Generada por la IA:
```json
[
  {
    "model": "academic.teacher",
    "pk": 1,
    "fields": {
      "first_name": "Marcelo",
      "last_name": "Alvarado"
    }
  },
  {
    "model": "academic.teacher",
    "pk": 2,
    "fields": {
      "first_name": "Carolina",
      "last_name": "Herrera"
    }
  },
  {
    "model": "academic.course",
    "pk": 1,
    "fields": {
      "name": "Desarrollo Backend con Python y Django",
      "teacher": 1
    }
  },
  {
    "model": "academic.student",
    "pk": 1,
    "fields": {
      "first_name": "Rodrigo",
      "last_name": "Gallardo"
    }
  },
  {
    "model": "academic.studentcourse",
    "pk": 1,
    "fields": {
      "student": 1,
      "course": 1
    }
  }
]
```

---

## Prompt 3: Maquetación y Diseño de Plantillas HTML con Bootstrap 5

### 📥 Prompt Enviado:
```text
Diseña una plantilla base 'base.html' y vistas hijas 'courses.html' y 'students.html' utilizando Bootstrap 5.3 CDN y Bootstrap Icons.
Requisitos:
- Diseño limpio, moderno y responsivo con paleta de colores profesional.
- Barra de navegación con enlaces a Inicio, Cursos, Estudiantes y menú dropdown con accesos a la API REST de DRF y Django Admin.
- Componentes de spinner de carga (loading state) y tarjetas de alerta para control de errores de red.
- Tablas estilizadas con badges visuales para las asignaturas y profesores.
```

### 📤 Respuesta Generada por la IA:
La IA proporcionó la estructura semántica completa con:
1. `base.html` con Navbar responsivo, contenedor `<main>` y footer institucional.
2. `courses.html` con contenedor para spinner `#loadingState`, mensaje de error `#errorState` y tabla interactiva `#coursesTable`.
3. `students.html` con soporte de etiquetas badge para renderizar los cursos inscritos de cada estudiante.

---

## Prompt 4: Implementación de Código Asíncrono con JavaScript Fetch API

### 📥 Prompt Enviado:
```text
Escribe el código JavaScript dentro de las plantillas de Django para consumir de manera asíncrona mediante fetch() los endpoints REST '/api/courses/' y '/api/students/'.
Requisitos:
- Uso de async/await y manejo de excepciones try/catch.
- Ocultar el spinner de carga una vez obtenidos los datos.
- Manipular el DOM para crear filas <tr> dinámicamente.
- Incluir un campo de filtro en tiempo real para buscar registros sin recargar la página.
- Agregar botón de recarga manual de datos.
```

### 📤 Respuesta Generada por la IA:
```javascript
async function fetchCourses() {
    loadingState.classList.remove('d-none');
    coursesTable.classList.add('d-none');
    try {
        const response = await fetch('/api/courses/');
        if (!response.ok) throw new Error(`HTTP Error ${response.status}`);
        const data = await response.json();
        renderTable(data);
    } catch (error) {
        console.error(error);
        loadingState.classList.add('d-none');
        errorState.classList.remove('d-none');
    }
}
```

---

## Prompt 5: Resolución de la Ruta Raíz '/' y Eliminación del Error 404

### 📥 Prompt Enviado:
```text
¿Cómo elimino el error 404 cuando el usuario accede a la raíz del servidor 'http://127.0.0.1:8000/' en Django?
Quiero una vista de dashboard/inicio estilizada con enlaces rápidos que explique la arquitectura de enmascaramiento de endpoints.
```

### 📤 Respuesta Generada por la IA:
La IA propuso:
1. Definir una vista `index_view(request)` en `academic/views.py` que retorne `render(request, 'academic/index.html', context)`.
2. Mapear `path('', index_view, name='home')` en `academic/urls.py` e incluir `path('', include('academic.urls'))` en `academic_project/urls.py`.
3. Crear `index.html` con un dashboard moderno con tarjetas de acceso directo y ficha de evaluación.
