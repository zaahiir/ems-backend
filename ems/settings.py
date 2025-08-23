from pathlib import Path
from datetime import timedelta
import os
import logging
import logging.config


BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-05k%mpd+p8b!wb$-w4^hj0qkmm^tn+@*i9$0tl11sdmsq@nn3)')


# Default to 'production' on the server; override with DJANGO_ENVIRONMENT=development locally
# ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'production')  # 'development' or 'production'
ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ENVIRONMENT == 'development'

# Define IS_PRODUCTION for consistent use throughout the file
IS_PRODUCTION = ENVIRONMENT == 'production'

ALLOWED_HOSTS = (
    ['66.179.189.41', 'backend.faiop.com', 'faiop.com', 'www.faiop.com']
    if IS_PRODUCTION
    else ['localhost', '127.0.0.1']
)

CORS_ALLOW_CREDENTIALS = True

# CORS/CSRF configuration per environment
DEV_CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',
    'http://localhost:3000',
    'http://127.0.0.1:4200',
]
PROD_CORS_ALLOWED_ORIGINS = [
    'https://faiop.com',
    'https://www.faiop.com',
    'https://backend.faiop.com',
]

CORS_ALLOWED_ORIGINS = (
    PROD_CORS_ALLOWED_ORIGINS if IS_PRODUCTION else DEV_CORS_ALLOWED_ORIGINS
)

CSRF_TRUSTED_ORIGINS = (
    [
        'https://faiop.com',
        'https://www.faiop.com',
        'https://backend.faiop.com',
    ]
    if IS_PRODUCTION
    else [
        'http://localhost:4200',
        'http://localhost:3000',
        'http://127.0.0.1:4200',
    ]
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'django_countries',
    'apis',
    'django_celery_beat',
    'django_celery_results',  # Enable Celery result backend
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

DATABASES = (
    # Development DB (existing settings in this file)
    {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'ems',
            'USER': 'xoft',
            'PASSWORD': '$martXoft@14',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    if not IS_PRODUCTION
    else
    # Production DB (as provided)
    {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'admin_test',
            'USER': 'mfs',
            'PASSWORD': '9Q39v5!dc',
            'HOST': 'backend.faiop.com',
            'PORT': '5432',
        }
    }
)



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
STATIC_ROOT = (
    '/var/www/vhosts/faiop.com/httpdocs/django/site/public/static'
    if IS_PRODUCTION
    else os.path.join(BASE_DIR, 'static/')
)

MEDIA_URL = '/media/'
MEDIA_ROOT = (
    '/var/www/vhosts/faiop.com/httpdocs/django/site/public/media'
    if IS_PRODUCTION
    else os.path.join(BASE_DIR, 'media/')
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MIME_TYPES = {
    'mp4': 'video/mp4',
    'pdf': 'application/pdf',
}

# Celery settings
CELERY_BROKER_URL = (
    'redis://backend.faiop.com:6379/0'
    if IS_PRODUCTION
    else 'redis://localhost:6379/0'
)

CELERY_RESULT_BACKEND = (
    'redis://backend.faiop.com:6379/1'
    if IS_PRODUCTION
    else 'redis://localhost:6379/1'
)

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'
CELERY_ENABLE_UTC = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Optional: Routing tasks to different queues
CELERY_TASK_ROUTES = {
    'apis.tasks.fetch_daily_nav': {'queue': 'nav_tasks'},
    # Add more tasks and queues as needed
}

CELERY_QUEUES = {
    'default': {
        'exchange': 'default',
        'binding_key': 'default',
    },
}


# For Celery result backend (optional)
CELERY_RESULT_BACKEND = (
    'redis://backend.faiop.com:6379/1'
    if IS_PRODUCTION
    else 'redis://localhost:6379/1'
)

CELERY_CACHE_BACKEND = 'django-cache'

