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

### Vistas Web (Frontend Enmascarado y Control de Acceso):
| Ruta | Tipo de Acceso | Descripción | Operaciones Soportadas |
| :--- | :--- | :--- | :--- |
| `http://127.0.0.1:8000/` | **Público / Abierto** | **Vista Gratuita (Landing & Demo)**: Explica el proyecto, arquitectura y catálogo. | Demostración y enlaces a Login/Docs. |
| `http://127.0.0.1:8000/login/` | **Público / Abierto** | **Inicio de Sesión**: Formulario de autenticación de usuarios. | Login con redirección inteligente `?next=`. |
| `http://127.0.0.1:8000/logout/` | **Público / Abierto** | **Cierre de Sesión**: Cierra sesión y retorna al inicio. | Logout de sesión activa. |
| `http://127.0.0.1:8000/docs/` | **Público / Abierto** | **Documentación Swagger UI**: Pruebas interactivas de la API. | Visualización y test de endpoints REST. |
| `http://127.0.0.1:8000/teachers/` | 🔒 **Requiere Login** | **Docentes**: CRUD interactivo de profesores. | **Crear**, **Listar**, **Editar**, **Eliminar**. |
| `http://127.0.0.1:8000/courses/` | 🔒 **Requiere Login** | **Cursos**: CRUD interactivo de asignaturas con profesor asignado. | **Crear**, **Listar**, **Editar**, **Eliminar**. |
| `http://127.0.0.1:8000/students/` | 🔒 **Requiere Login** | **Estudiantes**: CRUD de alumnos y gestión de inscripciones de materias. | **Crear**, **Listar**, **Editar**, **Eliminar**, **Inscribir/Desinscribir**. |

### Endpoints REST API (Django REST Framework):
| Endpoint | Métodos HTTP | Descripción |
| :--- | :--- | :--- |
| `http://127.0.0.1:8000/docs/` | `GET` | Interfaz interactiva Swagger UI de la API. |
| `http://127.0.0.1:8000/openapi/` | `GET` | Esquema OpenAPI en formato JSON. |
| `http://127.0.0.1:8000/api/token/` | `POST` | Obtención de tokens JWT (`access` y `refresh`) con credenciales. |
| `http://127.0.0.1:8000/api/token/refresh/` | `POST` | Renovación de token de acceso JWT vencido. |
| `http://127.0.0.1:8000/api/teachers/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD de Docentes (filtros: `first_name`, `last_name`, `search`, `ordering`). |
| `http://127.0.0.1:8000/api/courses/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD de Asignaturas (filtros: `teacher`, `name`, `search`, `ordering`). |
| `http://127.0.0.1:8000/api/students/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD de Estudiantes (filtros: `first_name`, `last_name`, `search`, `ordering`). |
| `http://127.0.0.1:8000/api/student-courses/` | `GET`, `POST`, `PUT`, `PATCH`, `DELETE` | CRUD de Inscripciones (filtros: `student`, `course`). |
| `http://127.0.0.1:8000/admin/` | `GET`, `POST` | Panel de Administración de Django. |

---

## 🧠 Preparación para la Interrogación (Criterio 10 - 6 Puntos)

A continuación se presentan las respuestas modelo para la defensa oral del proyecto:

### ❓ Pregunta 1: ¿Qué es el "enmascaramiento" de endpoints y cómo se implementó en este proyecto?
> **Respuesta:**  
> El "enmascaramiento" consiste en separar la capa de presentación visual (HTML/CSS) de la capa de entrega de datos (API REST JSON). En lugar de que Django renderice los datos del servidor directamente dentro de la plantilla usando variables de contexto como `{{ cursos }}`, Django únicamente entrega la estructura visual básica (`courses.html`, `students.html`). Luego, el navegador ejecuta código JavaScript con la función asíncrona `fetch('/api/courses/')` que solicita los datos JSON en segundo plano y manipula dinámicamente el DOM de la tabla. Esto desacopla el frontend del backend y permite una experiencia de usuario fluida y reactiva sin recargar la página.

### ❓ Pregunta 2: ¿Cómo se estructuraron las relaciones del modelo Entidad-Relación en Django (`models.py`)?
> **Respuesta:**  
> Se implementaron cuatro clases que heredan de `models.Model`:
> 1. `Teacher`: Entidad principal con `first_name` y `last_name`.
> 2. `Course`: Posee una clave foránea `teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses', db_column='teacher_id')` que representa la relación 1 a Muchos ("un profesor imparte una o más asignaturas").
> 3. `Student`: Entidad con `first_name` y `last_name`.
> 4. `StudentCourse`: Representa la tabla intermedia de la relación Muchos a Muchos entre `Student` y `Course`. Posee claves foráneas a ambas entidades y un `unique_together = ('student', 'course')` en su clase `Meta` para evitar inscripciones duplicadas.

### ❓ Pregunta 3: ¿Qué rol cumplen los Serializadores (`serializers.py`) en Django REST Framework?
> **Respuesta:**  
> Los serializadores actúan como traductores bidireccionales entre los tipos de datos complejos de Python (instancias de modelos Django y QuerySets) y formatos nativos como JSON, XML o diccionarios Python.  
> En este proyecto usamos `serializers.ModelSerializer`, y agregamos campos calculados como `teacher_name = serializers.CharField(source='teacher.full_name', read_only=True)` en `CourseSerializer` y `enrolled_courses` en `StudentSerializer` para que la respuesta JSON incluya directamente la información relacional enriquecida sin requerir múltiples consultas separadas desde el cliente.

### ❓ Pregunta 4: ¿Cómo se solucionó el error 404 en la ruta raíz `"/"` y cómo funciona el fallback de datos?
> **Respuesta:**  
> - Para el error 404: Se definió la vista `index_view` en `academic/views.py` y se registró la ruta vacía `path('', index_view, name='home')` en `academic/urls.py`, la cual se incluye en `academic_project/urls.py` mediante `path('', include('academic.urls'))`. De esta forma, al ingresar a `http://127.0.0.1:8000/`, el servidor devuelve un panel dashboard de inicio con código de estado HTTP 200.
> - Para el fallback: Los `ViewSets` en `views.py` verifican si existen registros en la base de datos relacional (`queryset.exists()`). Si la base de datos está vacía, retornan de forma transparente las colecciones estructuradas en memoria desde `mock_data.py`, garantizando que la API siempre responda con datos válidos ante cualquier escenario.

### ❓ Pregunta 5: ¿Cómo funciona la autenticación con Tokens JWT (`SimpleJWT`) integrada en el proyecto?
> **Respuesta:**  
> La autenticación JWT (*JSON Web Tokens*) es un mecanismo sin estado (*stateless*). En `urls.py` expusimos el endpoint `POST /api/token/` (`TokenObtainPairView`), donde el cliente envía sus credenciales (`username` y `password`) y el servidor le retorna un **Access Token** (con vigencia de 15 minutos) y un **Refresh Token** (con vigencia de 1 día). Para acceder a recursos protegidos, el cliente envía en los encabezados HTTP: `Authorization: Bearer <access_token>`. Cuando el token de acceso expira, se utiliza el endpoint `POST /api/token/refresh/` para obtener un nuevo token de acceso sin solicitar nuevamente la contraseña al usuario.

### ❓ Pregunta 6: ¿Cómo funcionan los filtros en los endpoints con `django-filter` y `SearchFilter`?
> **Respuesta:**  
> Configuramos `DjangoFilterBackend` y `SearchFilter` en `REST_FRAMEWORK` de `settings.py` y en cada `ViewSet`. Esto permite que el cliente agregue parámetros de consulta en la URL, por ejemplo:
> - Filtrar cursos por profesor: `GET /api/courses/?teacher=1`
> - Búsqueda por texto: `GET /api/courses/?search=Backend`
> - Ordenamiento: `GET /api/courses/?ordering=-id`
> El ViewSet ejecuta `self.filter_queryset(self.get_queryset())`, aplicando las cláusulas `WHERE` correspondientes en SQL de forma automática y optimizada.

---

## 👨‍💻 Autor
- **Estudiante:** Rodrigo Gallardo
- **Evaluación:** Evaluación N°1 - Desarrollo Backend con Django & DRF
- **Docente:** Marcelo Alvarado
