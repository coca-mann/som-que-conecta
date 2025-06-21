from pathlib import Path
from decouple import config, Csv
from datetime import timedelta
import os
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')

DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'backend.accounts.apps.AccountsConfig',
    'backend.instruments.apps.InstrumentsConfig',
    'backend.articles.apps.ArticlesConfig',
    'backend.lessons.apps.LessonsConfig',
    'backend.notifications.apps.NotificationsConfig',
    'backend.core.apps.CoreConfig',
    'corsheaders',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'django_filters',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'backend.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('PSQL_DB'),
        'USER': config('PSQL_USER'),
        'PASSWORD': config('PSQL_PASSWORD'),
        'HOST': config('PSQL_HOST'),
        'PORT': config('PSQL_PORT'),
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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Porto_Velho'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_EMAIL_REQUIRED = False

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

AUTHENTICATION_BACKENDS = [
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

REST_AUTH = {
    'PASSWORD_RESET_SERIALIZER': 'backend.accounts.serializers.CustomPasswordResetSerializer',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

# CORS settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]
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
]
CSRF_TRUSTED_ORIGINS = [
    'https://somqueconecta.fun',
    'https://admin.somqueconecta.fun',
    'https://www.somqueconecta.fun' # Boa prática adicionar o www também
]

USE_X_FORWARDED_HOST = config('USE_X_FORWARDED_HOST')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE')
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE')

SITE_ID = 1

ACCOUNT_ADAPTER = 'backend.accounts.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'backend.accounts.adapters.SocialAccountAdapter'
PASSWORD_RESET_CONFIRM_URL = '/password-reset-confirm/{uidb64}/{token}/'

SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # Não estamos usando um campo 'username'
ACCOUNT_EMAIL_REQUIRED = True             # O email é obrigatório
ACCOUNT_UNIQUE_EMAIL = True               # Cada email deve ser único
ACCOUNT_USERNAME_REQUIRED = False         # O 'username' não é obrigatório
ACCOUNT_AUTHENTICATION_METHOD = 'email'   # O método de autenticação é o email
ACCOUNT_EMAIL_VERIFICATION = 'optional' # 'mandatory' para forçar verificação de email


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'accounts.User'

# Google Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')

# --- CONFIGURAÇÃO DE E-MAIL ---
# Use o backend SMTP do Django
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Informações do seu provedor (exemplo com Brevo)
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_USE_TLS = config('EMAIL_USE_TLS')

# Suas credenciais (lidas das variáveis de ambiente)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# E-mail padrão que aparecerá como remetente
DEFAULT_FROM_EMAIL = 'Som que Conecta <nao-responda@somqueconecta.fun>'

FRONTEND_URL=config('FRONTEND_URL')
