# Evaluación N°1: Desarrollo Backend con Django & DRF

**Asignatura:** Desarrollo Backend  
**Docente:** Marcelo Alvarado  
**Estudiante:** Rodrigo Gallardo  
**Ponderación:** 15% de la Nota Final  
**Proyecto:** Sistema de Gestión Académica (`academic_project` / `academic`)  

---

## 📌 Descripción del Proyecto

Este proyecto corresponde al desarrollo del cascarón backend y frontend de una plataforma de gestión académica utilizando **Django 6.1** y **Django REST Framework (DRF)**.

La arquitectura implementa el patrón de **"enmascaramiento de endpoints REST"**: el usuario navega visualmente a través de vistas HTML estilizadas con **Bootstrap 5**, mientras que el navegador consume de manera asíncrona los datos en formato JSON desde los endpoints de DRF en segundo plano utilizando JavaScript (`fetch`).

---

## 🗂️ Estructura del Proyecto

```text
RodrigoGallardo/
│
├── academic_project/             # Directorio de configuración global de Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py               # Configuración (INSTALLED_APPS, TEMPLATES, DRF, DB)
│   ├── urls.py                   # Enrutamiento principal (incluye app 'academic' y admin)
│   └── wsgi.py
│
├── academic/                     # Aplicación de Gestión Académica
│   ├── migrations/               # Migraciones de base de datos
│   │   └── 0001_initial.py
│   ├── fixtures/                 # Datos ficticios de prueba en JSON
│   │   └── initial_data.json
│   ├── templates/academic/       # Plantillas HTML
│   │   ├── base.html             # Plantilla base con Bootstrap 5.3 CDN y Navbar
│   │   ├── index.html            # Dashboard de bienvenida (elimina error 404 en '/')
│   │   ├── courses.html          # Vista de Cursos (consume /api/courses/ con fetch)
│   │   └── students.html         # Vista de Estudiantes (consume /api/students/ con fetch)
│   ├── admin.py                  # ModelAdmin para panel administrativo
│   ├── apps.py                   # Configuración de la aplicación
│   ├── mock_data.py              # Datos simulados y colecciones en memoria
│   ├── models.py                 # Modelos ER (Teacher, Course, Student, StudentCourse)
│   ├── serializers.py            # Serializadores DRF (ModelSerializer)
│   ├── tests.py                  # Pruebas unitarias automatizadas (11 tests)
│   ├── urls.py                   # Rutas de vistas HTML y endpoints DRF
│   └── views.py                  # Vistas de renderizado HTML y ViewSets DRF
│
├── db.sqlite3                    # Base de datos relacional SQLite precargada
├── manage.py                     # Script de gestión de Django
├── prompts.md                    # Entregable de Inteligencia Artificial (registro de prompts)
├── .gitignore                    # Reglas de exclusión para Git
└── README.md                     # Documentación general y guía de interrogación
```

---

## 🚀 Instrucciones de Instalación y Ejecución

### 1. Requisitos Previos
- Python 3.10 o superior (verificado con Python 3.14)
- Django y Django REST Framework instalados:
  ```bash
  pip install django djangorestframework
  ```

### 2. Aplicar Migraciones
```bash
python manage.py makemigrations academic
python manage.py migrate
```

### 3. Cargar Datos de Prueba (Fixtures)
Para cargar los docentes, asignaturas, estudiantes e inscripciones iniciales:
```bash
python manage.py loaddata academic/fixtures/initial_data.json
```

### 4. Ejecutar Pruebas Automatizadas
Para validar que todos los modelos, vistas y endpoints funcionan al 100%:
```bash
python manage.py test
```

### 5. Iniciar el Servidor de Desarrollo
```bash
python manage.py runserver
```
El sistema quedará disponible en: **`http://127.0.0.1:8000/`**

### 🔐 Credenciales del Panel de Administración (`/admin/`):
- **URL:** `http://127.0.0.1:8000/admin/`
- **Usuario:** `admin`
- **Contraseña:** `admin`
- **Email:** `admin@academic.cl`

---

## 🌐 Mapeo de Rutas y Endpoints

### Vistas Web (Frontend Enmascarado con CRUD Completo):
| Ruta | Descripción | Operaciones Soportadas |
| :--- | :--- | :--- |
| `http://127.0.0.1:8000/` | **Inicio / Dashboard**: Resuelve la raíz y elimina el error 404. | Lectura y accesos directos. |
| `http://127.0.0.1:8000/teachers/` | **Docentes**: CRUD interactivo de profesores. | **Crear**, **Listar**, **Editar**, **Eliminar**. |
| `http://127.0.0.1:8000/courses/` | **Cursos**: CRUD interactivo de asignaturas con profesor asignado. | **Crear**, **Listar**, **Editar**, **Eliminar**. |
| `http://127.0.0.1:8000/students/` | **Estudiantes**: CRUD de alumnos y gestión de inscripciones de materias. | **Crear**, **Listar**, **Editar**, **Eliminar**, **Inscribir/Desinscribir**. |

### Endpoints REST API (Django REST Framework):
| Endpoint | Métodos HTTP | Descripción |
| :--- | :--- | :--- |
| `http://127.0.0.1:8000/api/teachers/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD completo para Docentes. |
| `http://127.0.0.1:8000/api/courses/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD completo para Asignaturas. |
| `http://127.0.0.1:8000/api/students/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD completo para Estudiantes. |
| `http://127.0.0.1:8000/api/student-courses/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD para Inscripciones de Estudiantes a Cursos. |
| `http://127.0.0.1:8000/admin/` | `GET`, `POST` | Panel de Administración de Django. |

---

## 👨‍💻 Autor
- **Estudiante:** Rodrigo Gallardo
- **Evaluación:** Evaluación N°1 - Desarrollo Backend con Django & DRF
- **Docente:** Marcelo Alvarado
