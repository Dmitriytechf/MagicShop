import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# Оплата stripe
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET')


DEBUG = True

ALLOWED_HOSTS = ['*']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # additionally
    'mathfilters',
    'crispy_forms',
    'crispy_bootstrap5',
    'django_email_verification',
    'sorl.thumbnail',
    'django_celery_beat',
    'django_celery_results',
    'django_htmx',
    'rest_framework',
    'djoser',
    'drf_yasg',
    
    # apps
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'account.apps.AccountConfig',
    'payment.apps.PaymentConfig',
    'mainpage.apps.MainpageConfig',
    'otherapp.apps.OtherappConfig',
    'api.apps.ApiConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bigcorp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mainpage'/ 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # Добавляем наш контекст процессор
                'shop.context_processors.categories',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'bigcorp.wsgi.application'


# База данных(пока sqlite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# Настройки часовой зоны и языка
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статика и медиа
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_DIRS = [
    BASE_DIR / 'mainpage' / 'static',
    BASE_DIR / 'payment' / 'static',
]

MEDIA_URL = '/media/'  # URL для доступа к медиафайлам
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

LOGIN_REDIRECT_URL = 'shop:products'  # Куда перенаправлять после входа
LOGOUT_REDIRECT_URL = 'shop:products'  # Куда перенаправлять после выхода


# Celery
CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TIMEZONE = 'UTC'

CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Email для теста
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# REST_FRAMEWORK 
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '100000/day',
        'anon': '10000/day',
    },
    "DEFAULT_PERMISSION_CLASSES": [
        "api.permissions.IsAdminOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "api.pagination.StandardResultsSetPagination",
    "PAGE_SIZE": 15,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

DJOSER = {
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "user_create": "api.serializers.UserCreateSerializer",
    },
    'AUTH_HEADER_TYPES': ('JWT',),

}


# Здесь все что касается настроек авторизации по email(пока не нужно)
# def email_verified_callback(user):
#     user.is_active = True

# def password_change_callback(user, password):
#     user.set_password(password)

# # Global Package Settings
# EMAIL_FROM_ADDRESS = 'noreply@aliasaddress.com'  # mandatory
# EMAIL_PAGE_DOMAIN = 'https://mydomain.com/'  # mandatory (unless you use a custom link)
# EMAIL_MULTI_USER = False  # optional (defaults to False)

# # Email Verification Settings (mandatory for email sending)
# EMAIL_MAIL_SUBJECT = 'Confirm your email {{ user.username }}'
# EMAIL_MAIL_HTML = 'mail_body.html'
# EMAIL_MAIL_PLAIN = 'mail_body.txt'
# EMAIL_MAIL_TOKEN_LIFE = 60 * 60  # one hour

# # Email Verification Settings (mandatory for builtin view)
# EMAIL_MAIL_PAGE_TEMPLATE = 'email_success_template.html'
# EMAIL_MAIL_CALLBACK = email_verified_callback

# # Password Recovery Settings (mandatory for email sending)
# EMAIL_PASSWORD_SUBJECT = 'Change your password {{ user.username }}'
# EMAIL_PASSWORD_HTML = 'password_body.html'
# EMAIL_PASSWORD_PLAIN = 'password_body.txt'
# EMAIL_PASSWORD_TOKEN_LIFE = 60 * 10  # 10 minutes

# # Password Recovery Settings (mandatory for builtin view)
# EMAIL_PASSWORD_PAGE_TEMPLATE = 'password_changed_template.html'
# EMAIL_PASSWORD_CHANGE_PAGE_TEMPLATE = 'password_change_template.html'
# EMAIL_PASSWORD_CALLBACK = password_change_callback

# # For Django Email Backend
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'mymail@gmail.com'
# EMAIL_HOST_PASSWORD = 'mYC00lP4ssw0rd'  # os.environ['password_key'] suggested
# EMAIL_USE_TLS = True


# Настройка логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        # 'file': {
        #     'level': 'DEBUG',
        #     'class': 'logging.FileHandler',
        #     'filename': '/var/log/celery/tasks.log',
        # },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime}[{levelname}]: {message} | ({module})',
            'style': '{',
        },
    },
    'loggers': {
        'bigcorp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
