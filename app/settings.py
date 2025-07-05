# settings.py

from decouple import config
import os
from pathlib import Path

# Log inicial para ver se o arquivo está sendo lido
print("DEBUG: settings.py started loading.")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(f"DEBUG: BASE_DIR is set to: {BASE_DIR}")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')
# Não printar SECRET_KEY por segurança, mas podemos ver se config está funcionando
print(f"DEBUG: SECRET_KEY loaded (length: {len(SECRET_KEY) if SECRET_KEY else 0})")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)
print(f"DEBUG: DEBUG is set to: {DEBUG}")

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1').split(',')
print(f"DEBUG: ALLOWED_HOSTS are: {ALLOWED_HOSTS}")
GOOGLE_API_TOKEN = config("GOOGLE_API_TOKEN")
print(f"DEBUG: GOOGLE_API_TOKEN loaded (length: {len(GOOGLE_API_TOKEN) if GOOGLE_API_TOKEN else 0})")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # <--- Verifique se staticfiles está aqui
    'emails'
]
print(f"DEBUG: INSTALLED_APPS include 'django.contrib.staticfiles': {'django.contrib.staticfiles' in INSTALLED_APPS}")


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # <-- Mova para esta posição!
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
print("DEBUG: Middleware loaded.")


ROOT_URLCONF = 'app.urls'
print(f"DEBUG: ROOT_URLCONF is: {ROOT_URLCONF}")


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'base',
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
print("DEBUG: TEMPLATES loaded.")


WSGI_APPLICATION = 'app.wsgi.application'
print(f"DEBUG: WSGI_APPLICATION is: {WSGI_APPLICATION}")


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
print("DEBUG: DATABASES loaded.")


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
print("DEBUG: AUTH_PASSWORD_VALIDATORS loaded.")


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
print(f"DEBUG: Internationalization settings: LANGUAGE_CODE={LANGUAGE_CODE}, TIME_ZONE={TIME_ZONE}")


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
print(f"DEBUG: STATIC_URL is: {STATIC_URL}")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'base/static')
]
print(f"DEBUG: STATICFILES_DIRS is: {STATICFILES_DIRS}")
print(f"DEBUG: Does base/static exist locally? {os.path.exists(os.path.join(BASE_DIR, 'base/static'))}") # Checa se a pasta existe

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
print(f"DEBUG: STATIC_ROOT is set to: {STATIC_ROOT}") # ESSA É A MAIS IMPORTANTE

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
print(f"DEBUG: STATICFILES_STORAGE is: {STATICFILES_STORAGE}")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
print(f"DEBUG: DEFAULT_AUTO_FIELD is: {DEFAULT_AUTO_FIELD}")

print("DEBUG: settings.py finished loading.")