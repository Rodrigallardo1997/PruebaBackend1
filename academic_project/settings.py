"""
Django settings for academic_project project.

Evaluación N°1: Desarrollo Backend con Django & DRF
Estudiante: Rodrigo Gallardo
Docente: Marcelo Alvarado

Este archivo contiene la configuración global del proyecto Django.
Se registran las aplicaciones 'rest_framework' (Django REST Framework)
y la app 'academic' correspondiente al dominio de gestión académica.
"""

from pathlib import Path
import os

# Ruta base del proyecto (directorio raíz)
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta para desarrollo (en producción debe mantenerse privada mediante variables de entorno)
SECRET_KEY = 'django-insecure-rd(k_d3k#k31n*)e*fim^2_1e!()kq*$w7@j5tg(xluwe#k@u&'

# Modo depuración activo para desarrollo
DEBUG = True

# Hosts permitidos para atender peticiones HTTP
ALLOWED_HOSTS = ['*']


# ==============================================================================
# DEFINICIÓN DE APLICACIONES INSTALADAS
# ==============================================================================
INSTALLED_APPS = [
    # Aplicaciones estándar de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Paquete externo: Django REST Framework (DRF) para creación de APIs REST
    'rest_framework',

    # Aplicación local: Sistema de Gestión Académica
    'academic',
]

# ==============================================================================
# MIDDLEWARE
# ==============================================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración del archivo de URLs principal
ROOT_URLCONF = 'academic_project.urls'

# ==============================================================================
# CONFIGURACIÓN DE PLANTILLAS (TEMPLATES)
# ==============================================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Directorios adicionales de búsqueda de plantillas HTML
        'DIRS': [
            BASE_DIR / 'academic' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Aplicación WSGI para servidores web
WSGI_APPLICATION = 'academic_project.wsgi.application'


# ==============================================================================
# BASE DE DATOS (SQLite relacional por defecto)
# ==============================================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# VALIDACIÓN DE CONTRASEÑAS
# ==============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ==============================================================================
# INTERNACIONALIZACIÓN Y ZONA HORARIA
# ==============================================================================
LANGUAGE_CODE = 'es-cl'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_TZ = True


# ==============================================================================
# ARCHIVOS ESTÁTICOS (CSS, JavaScript, Imágenes)
# ==============================================================================
STATIC_URL = '/static/'

# ==============================================================================
# CONFIGURACIÓN DE DJANGO REST FRAMEWORK
# ==============================================================================
REST_FRAMEWORK = {
    # Renderers por defecto (JSON y Navegador interactivo de DRF)
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # Formato de respuesta estándar
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

