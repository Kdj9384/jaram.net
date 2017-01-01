import os

from os.path import join

BASE_DIR = join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/
SECRET_KEY = '0mw@e)h5k=t6)&a5qgw*rbom5vt3qseqst&z70rpvqjl(cy9gx'

DEBUG = False

MANAGERS = (
    ('JinYong Kim', 'jinyong@jadekim.kr'),
)

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
]

JARAM_APPS = [
    'main',
    'board',
    'study',
    'gallery',
    'schedule',
    'workshop',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'django_cleanup',
    # 'mod_wsgi.server'
]

INSTALLED_APPS = DJANGO_APPS + JARAM_APPS + THIRD_PARTY_APPS

CKEDITOR_UPLOAD_PATH = 'ckeditor/files/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': None,
    },
}

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'main.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'jaram.urls'

WSGI_APPLICATION = 'jaram.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
}

AUTH_USER_MODEL = 'main.Member'
LOGIN_URL = '/login'
LOGOUT_URL = '/logout'
LOGIN_REDIRECT_URL = '/main'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators
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

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DATETIME_FORMAT = ('Y-m-d H:i:s',)
DATE_FORMAT = ('Y-m-d',)

SERVICE_HOST = "http://localhost:8000"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            'main/templates',
            'board/templates',
            'study/templates',
            'workshop/templates',
            'schedule/templates',
            'gallery/templates',
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

STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/jaram/static_root/'
STATICFILES_DIRS = (
    'main/static',
    'board/static',
    'workshop/static',
    'schedule/static',
    'gallery/static',
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

URL = 'http://localhost:8000'

EXCLUDE_LOGIN_REQUIRED_URLS = [
    r'^$|^intro',
    r'^login',
    r'^logout',
    r'^sign_up',
    r'^admin',
]
