from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-...'
DEBUG = True
ALLOWED_HOSTS = []

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'school_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # مجلد templates عام
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

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}



AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# اللغة والتوقيت
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Amman'
USE_I18N = True
USE_TZ = True

# ملفات ثابتة وإعلامية
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'core.User'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/core/'
LOGOUT_REDIRECT_URL = '/core/'

# يقرأ كل المتغيرات من ملف .env
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

# إعدادات البريد الإلكتروني باستخدام SMTP لجيميل
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'taalomifiyadi@gmail.com'  # البريد الذي سيرسل منه
EMAIL_HOST_PASSWORD = 'lldj gobi dorn zfhr'  # كلمة مرور التطبيق (وليس كلمة مرور الحساب العادية)
DEFAULT_FROM_EMAIL = 'تعلمي في يدي <taalomifiyadi@gmail.com>'

AUTH_USER_MODEL = 'core.User'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# مسار ملفات static العادية (CSS, JS, صور)
STATIC_URL = '/static/'
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'ta3lemi-fi-yadi.onrender.com', '.onrender.com']
CSRF_TRUSTED_ORIGINS = [
    "https://ta3lemi-fi-yadi.onrender.com",
    "http://ta3lemi-fi-yadi.onrender.com",
]

