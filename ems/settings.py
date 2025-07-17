# settings.py fixes

from pathlib import Path
from datetime import timedelta
import os

# Setup base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-05k%mpd+p8b!wb$-w4^hj0qkmm^tn+@*i9$0tl11sdmsq@nn3)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Changed to True for debugging purposes

ALLOWED_HOSTS = ['66.179.189.41', 'backend.faiop.com', 'localhost', '127.0.0.1', 'faiop.com', 'www.faiop.com']

# HTTPS settings - Disable for debugging CORS issues
SESSION_COOKIE_SECURE = False  # Set to False for debugging
CSRF_COOKIE_SECURE = False     # Set to False for debugging
SECURE_SSL_REDIRECT = False

# HSTS Settings - Disable for debugging
SECURE_HSTS_SECONDS = 0        # Set to 0 for debugging
SECURE_HSTS_PRELOAD = False
SECURE_HSTS_INCLUDE_SUBDOMAINS = False

# CORS Settings - Fixed and expanded
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False  # Set to True temporarily for debugging if needed

CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://localhost:3000',
    'http://127.0.0.1:4200',
    'http://127.0.0.1:3000',
    'https://faiop.com',
    'https://www.faiop.com',
    'https://backend.faiop.com',
    'https://www.backend.faiop.com',
    'http://66.179.189.41',
    'https://66.179.189.41',
    'http://faiop.com',
    'http://www.faiop.com',
]

# More detailed CORS settings
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'cache-control',
    'pragma',
]

# Add this to handle preflight requests
CORS_PREFLIGHT_MAX_AGE = 86400  # 24 hours

# Additional CORS settings for debugging
CORS_EXPOSE_HEADERS = [
    'content-type',
    'x-csrftoken',
]

INSTALLED_APPS = [
    'corsheaders',  # Move corsheaders to the top
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_countries',
    'apis',
    'django_celery_beat',
    'django_celery_results',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Move to the very top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ems.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'ems.wsgi.application'

# Database settings with connection pooling
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'admin_test',
#         'USER': 'mfs',
#         'PASSWORD': '9Q39v5!dc',
#         'HOST': 'backend.faiop.com',
#         'PORT': '5432',
#         'OPTIONS': {
#             'connect_timeout': 30,
#             'options': '-c statement_timeout=30000'  # 30 seconds
#         },
#         'CONN_MAX_AGE': 600,  # Connection pooling
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ems',
        'USER': 'xoft',
        'PASSWORD': '$martXoft@14',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

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

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True
USE_L10N = True

STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/vhosts/faiop.com/httpdocs/django/site/public/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/vhosts/faiop.com/httpdocs/django/site/public/media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIME_TYPES = {
    'mp4': 'video/mp4',
    'pdf': 'application/pdf',
}

# Celery settings
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Optional: Routing tasks to different queues
CELERY_TASK_ROUTES = {
    'apis.tasks.fetch_daily_nav': {'queue': 'nav_tasks'},
}

CELERY_QUEUES = {
    'default': {
        'exchange': 'default',
        'binding_key': 'default',
    },
    'nav_tasks': {
        'exchange': 'nav_tasks',
        'binding_key': 'nav_tasks',
    },
}

# For Celery result backend
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# Add logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'corsheaders': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'apis': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}