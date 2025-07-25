from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent
TEMPLATES_DIR = BASE_DIR / "templates"
TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)


def is_running_in_docker():
    try:
        with open("/proc/1/cgroup", "rt") as f:
            return any("docker" in line or "containerd" in line for line in f)
    except FileNotFoundError:
        return False



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = os.environ.get("DJANGO_DEBUG")
DEBUG = False  


# Drone IDs from environment file
raw = os.environ.get('DRONE_IDS', '')
DRONE_IDS = [d.strip() for d in raw.split(',')] if raw else []

# MQTT Creds from environment file
MQTT_BROKER_URL = os.environ.get('MQTT_BROKER_URL', 'localhost')
MQTT_BROKER_PORT = int(os.environ.get('MQTT_BROKER_PORT', '1883'))
MQTT_CLIENT_ID = os.environ.get('MQTT_CLIENT_ID', '')

PROJECT_NAME = 'droneData'

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/data/'
LOGOUT_REDIRECT_URL = '/login/'

ALLOWED_HOSTS = [
    '*',
    'localhost',
    '127.0.0.1',                 
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'droneData.apps.DronedataConfig',
    'django.contrib.sites',
    'channels',
    'rest_framework',    
    'drf_spectacular',
]

REST_FRAMEWORK = {
    # YOUR SETTINGS
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'My First Sager Task',
    'DESCRIPTION': 'I made this project which recieves data from simulated drones using MQTT, then the project processes the data and displayes it on simple html pages using APIs. In addidition to having regular REST APIs to access the data, I have imoplemented a WebSocket API to allow real-time updates of the data on the web pages. The project also has an admin page and some pages require you to be logged in to access them.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
}

SITE_ID = 1

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CSRF_COOKIE_SECURE = True 

ROOT_URLCONF = 'task1.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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
## IN-MEMORY CHANNEL LAYER (DOES NOT WORK WITH ASGI(I THINK))
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer",
#     },
# }


## REDIS CHANNEL LAYER

REDIS_HOST = "redis" if is_running_in_docker() else "127.0.0.1"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, 6379)],
        },
    },
}


WSGI_APPLICATION = 'task1.wsgi.application'
ASGI_APPLICATION = "task1.asgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


## SQLITE DATABASE (DOES NOT WORK WITH ASGI)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dronedata',
        'USER': 'droneuser',
        'PASSWORD': 'dronepass',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

# AUTH_PASSWORD_VALIDATORS = [
#     {
#         'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#     },
#     {
#         'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#     },
# ]

AUTH_PASSWORD_VALIDATORS = []

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'                     # leading slash is important

STATICFILES_DIRS = [
    BASE_DIR / 'static',                    # points to src/static
]
STATIC_ROOT = BASE_DIR / 'task1' / 'staticfiles'
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
