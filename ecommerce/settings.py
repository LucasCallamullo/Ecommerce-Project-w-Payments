"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# =====================================================================================
#             EVERYTHING RELATED TO ENVIRONMENTAL VARIABLES n DB
# =====================================================================================
# Register pymysql as MySQL driver
import pymysql
pymysql.install_as_MySQLdb()

import environ, os
env = environ.Env()    # Init the environment

try:
    # In local we use environ to bring keys from the .env file, in "Railway" this does not work
    # as such and we must use the "except" block to configure correctly with the environment variables
    # that are added in the "Railway" panel
    environ.Env.read_env()
    MERCADO_PAGO_PUBLIC_KEY = env('MERCADO_PAGO_PUBLIC_KEY')
    MERCADO_PAGO_ACCESS_TOKEN = env('MERCADO_PAGO_ACCESS_TOKEN')
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = env('SECRET_KEY')
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = env('DEBUG')
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': env('MYSQL_DATABASE'),
            'USER': env('MYSQL_USER'),
            'PASSWORD': env('MYSQL_PASSWORD'),
            'HOST': env('MYSQL_HOST'),
            'PORT': env('MYSQL_PORT'),
        }
    }

except environ.ImproperlyConfigured:
    # This is for deploy on railway
    MERCADO_PAGO_PUBLIC_KEY = os.getenv('MERCADO_PAGO_PUBLIC_KEY', 'default_public_key')
    MERCADO_PAGO_ACCESS_TOKEN = os.getenv('MERCADO_PAGO_ACCESS_TOKEN', 'default_access_token')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    DEBUG = os.getenv('DEBUG', True)
    
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_DATABASE', 'railway'),
            'USER': os.getenv('MYSQL_USER', 'root'),
            'PASSWORD': os.getenv('MYSQL_PASSWORD', 'default_password'),
            'HOST': os.getenv('MYSQL_HOST', 'localhost'),
            'PORT': os.getenv('MYSQL_PORT', '53817'),
        }
    }
    
# =====================================================================================
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # for deploy
    'whitenoise.runserver_nostatic',
    'rest_framework',
    
    # My apps
    'home',
    'users',
    'cart',
    'products',
    'orders',
    'payments',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

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
                
                # This is my custom context_processors
                'products.context_processors.get_categories_n_subcats',
                'home.context_processors.get_ecommerce_data',
                'cart.context_processors.carrito_total',
                'users.context_processors.widget_register_form',
            ],
        },
    },
]

WSGI_APPLICATION = 'ecommerce.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,  # Longitud mínima de cuatro caracteres
        }
    },
]

AUTH_USER_MODEL = 'users.CustomUser'    # NOTE custom user for appWeb

""" 
Esto estaba antes en AUTH_PASSWORD_VALIDATORS = [
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
"""

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Ruta para archivos estaticos globales
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_URL = 'media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Add for deploy to use "Whitenoise"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# =======================================================================
#                        DRF SETTINGS STUFF 
# =======================================================================
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        # This allows you to view the API in HTML format (browser interface)
        'rest_framework.renderers.BrowsableAPIRenderer',  
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    
    # Esto es para usar drf con jwt (json web token)
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #    'rest_framework.authentication.BasicAuthentication',
    #    'rest_framework.authentication.SessionAuthentication',
    #),
}
# ====================================================================

# this is for deployment
# ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['127.0.0.1', 'web-production-8e84.up.railway.app']


CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1',
    'https://web-production-8e84.up.railway.app',
]

# CSRF_COOKIE_SECURE = True  # Railway usa HTTPS
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'None'  # Permitir cookies cross-site si es necesario
