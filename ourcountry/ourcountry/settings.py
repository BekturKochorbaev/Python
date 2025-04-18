from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True

ALLOWED_HOSTS = ["*"]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


INSTALLED_APPS = [
    'jazzmin',
    'modeltranslation',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'country',
    "phonenumber_field",
    'accounts',
    'rest_framework_swagger',
    'drf_yasg',
    'multiselectfield',
    "corsheaders",
    'rest_framework_simplejwt',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'django_rest_passwordreset',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # вот это обязательно

]

ROOT_URLCONF = 'ourcountry.urls'

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

WSGI_APPLICATION = 'ourcountry.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES["default"] = dj_database_url.parse("postgresql://postgres_p9n6_user:vUGizEIsSNLjHA32AxwT46dZvn6cPlxO@dpg-d00b9c2li9vc739nq5dg-a.singapore-postgres.render.com/postgres_p9n6")


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


CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    'https://cute-jalebi-1777db.netlify.app',
    'https://api.sitetrevel.online',
    'https://sitetrevel.online',

]

CORS_ALLOW_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']

CKEDITOR_CONFIGS = {
    'basic': {
        'toolbar': [
            ['Bold', 'Italic', 'Underline', '-',
             'NumberedList', 'BulletedList', '-',
             'JustifyLeft', 'JustifyCenter', 'JustifyRight',
             'Source'],
        ],
        'width': 'auto',
        'height': '200px',
        'removePlugins': 'elementspath',
        'toolbarCanCollapse': True,
        'uiColor': '#f0f0f0',
    },
    'default': {
        'toolbar': [
            ['Format', 'Font', 'FontSize', 'Bold', 'Italic', 'Underline', '-',
             'NumberedList', 'BulletedList', '-', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock', 'Image', 'Link', 'Unlink', 'Table',
             'Source', 'Maximize'],
        ],
        'width': 'auto',
        'height': '200px',
        'toolbarCanCollapse': True,
        'uiColor': '#f0f0f0',
        'removePlugins': 'elementspath',
        'extraPlugins': 'font,maximize',
        'fontSize_sizes': (
            '8/8px;9/9px;10/10px;11/11px;12/12px;14/14px;16/16px;18/18px;'
            '20/20px;22/22px;24/24px;26/26px;28/28px;36/36px;48/48px;72/72px'
        ),
        'font_names': (
            'Arial/Arial, Helvetica, sans-serif;'
            'Times New Roman/Times New Roman, Times, serif;'
            'Verdana'
        ),
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_IMAGE_BACKEND = "pillow"

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Asia/Bishkek'
USE_L10N = True
USE_I18N = True
USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
    ('ar', 'Arabic'),
)

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'ru', 'ar')


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    )
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'accounts.UserProfile'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=50),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'bekturkochorbaev64@gmail.com'
EMAIL_HOST_PASSWORD = 'diwd chov wdrx wepj'
