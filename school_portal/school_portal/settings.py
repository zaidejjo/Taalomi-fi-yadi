from pathlib import Path
from pickle import FALSE
from dotenv import load_dotenv
import dj_database_url
import os

# تحميل المتغيرات من .env
load_dotenv()

# مسار المشروع الأساسي
BASE_DIR = Path(__file__).resolve().parent.parent

# الأمان
SECRET_KEY = os.getenv("SECRET_KEY")  # غيّرها لمفتاحك الحقيقي
DEBUG = FALSE
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ta3lemi-fi-yadi.onrender.com', '.onrender.com']

SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True


# التطبيقات المثبتة
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'widget_tweaks',
    # تطبيقاتك الخاصة
    'core',
    'academics',
    'attendance',
    'transfers',
    'assignments',
    'competitions',
    'ai_chat',
    'audit',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ملفات القوالب
ROOT_URLCONF = 'school_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'school_portal.wsgi.application'

# قاعدة البيانات
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# Validators لكلمات المرور
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# إعدادات اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Amman'
USE_I18N = True
USE_TZ = True

# ملفات static و media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# إعدادات الحساب
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.User'
LOGIN_REDIRECT_URL = '/core/'
LOGOUT_REDIRECT_URL = '/core/'
LOGIN_URL = '/core/login/'

# بريد إلكتروني SMTP
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'taalomifiyadi@gmail.com'
EMAIL_HOST_PASSWORD = 'lldj gobi dorn zfhr'  # كلمة مرور التطبيق
DEFAULT_FROM_EMAIL = 'تعلمي في يدي <taalomifiyadi@gmail.com>'

# Trusted origins
CSRF_TRUSTED_ORIGINS = [
    "https://ta3lemi-fi-yadi.onrender.com",
    "http://ta3lemi-fi-yadi.onrender.com",
]


# مفتاح API لـ Cohere
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

