
from pathlib import Path
from decouple import config
from django import conf

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = Path.joinpath(BASE_DIR, 'templates')
STATIC_DIR = Path.joinpath(BASE_DIR, 'static')
MEDIA_DIR = Path.joinpath(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b^_6n4g+!@#69bs%pec-bp2o(db_ga_aj0%d@5#h=$*8egfm80'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

SECRET_KEY = config('THE_SECRET_KEY')
DEBUG = config('WEB_DEBUG', cast = bool)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'admin_tools_stats', 
    'django_nvd3',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history', 'lockdown', 'crispy_forms', 'crispy_bootstrap4',
    'defender',
    'App_Auth', 'App_Chat', 'App_Mail', 'App_Resume', 'App_Converter'

]

CRISPY_ALLOWED_TEMPLATE_PACKs = 'bootstrap4'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    # 'lockdown.middleware.LockdownMiddleware', # Lockdown an entire site
    'django_auto_logout.middleware.auto_logout', # Session log out
    # 'defender.middleware.FailedLoginMiddleware', # Failed login
    'App_Auth.middleware.HitCounterMiddleware', # hit Count
]

ROOT_URLCONF = 'Core.urls'

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
                'django_auto_logout.context_processors.auto_logout_client',
            ],
        },
    },
]

WSGI_APPLICATION = 'Core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': config('DATABASE_NAME'),
#         'HOST': config("DATABASE_HOST"),
#         'PORT': config("DATABASE_PORT"),
#         'USER': config("DATABASE_USER"),
#         'PASSWORD': config("DATABASE_PASSWORD"),
#     }
# }

AUTH_USER_MODEL = 'App_Auth.UserProfile'

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# STATIC_ROOT = ''

# STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = 'media/'
MEDIA_ROOT = MEDIA_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/signin/'

LOGIN_REDIRECT_URL = 'App_Auth/signin'
LOGOUT_REDIRECT_URL = 'App_Auth/signout'


from datetime import timedelta
AUTO_LOGOUT = {
    'IDLE_TIME': timedelta(minutes=30),
    #  'SESSION_TIME': timedelta(minutes=30),
    'REDIRECT_TO_LOGIN_IMMEDIATELY': True,
     'MESSAGE': 'The session has expired. Please login again to continue.',
}


# Send Mail 
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
EMAIL_HOST_USER = 'shovonmufrid98@gmail.com'
EMAIL_HOST_PASSWORD = 'dgsxxwcpogfrolvr'

### Lockdown Password
LOCKDOWN_PASSWORDS = ('letmein', 'beta')


### Cross Site Scripting 
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True

### Redirects all non-HTTPS requests to HTTP
# SECURE_SSL_REDIRECT = True

### HTTP Strict Transport Security
# SECURE_HSTS_SECONDS = 86400
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

### Cross-site request forgery(CSRF) protection
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

