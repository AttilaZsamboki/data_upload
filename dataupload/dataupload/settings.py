from pathlib import Path
import os
import dotenv

dotenv.load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure--@^%b3wauz8qkdive2s#o8pc+2)^d9)7%&!^=6=g1a6p6lab&5"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["www.dataupload.xyz", "164.92.166.60", "127.0.0.1"]

# Application definition

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "api",
    "django_crontab",
    "frontend.apps.FrontendConfig",
    "rest_framework",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = "dataupload.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dataupload.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "defaultdb",
        "USER": "doadmin",
        "PASSWORD": "AVNS_FovmirLSFDui0KIAOnu",
        "HOST": "defaultdb.c0rzdkeutp8f.eu-central-1.rds.amazonaws.com",
        "PORT": "25060",
    }
}

CRONJOBS = [
    ("*/10 * * * *", "api.cron.add_coupon_used_tag"),
    ("*/10 * * * *", "api.cron.upload_file"),
    ("0 * * * *", "api.cron.upload_feed_daily"),
    ("30 * * * *", "api.cron.upload_feed_hourly"),
    ("0 1 * * 5", "api.cron.upload_feed_weekly"),
    ("*/10 * * * *", "api.cron.email_uploads"),
    ("0 10 1 * *", "api.cron.upload_pro_stock_month"),
    ("0 12 1 * *", "api.cron.pro_stock_report_summary"),
    # ('0 0 * * *', 'api.cron.unas_upload_and_translate'),
    # ('0 0 * * *', 'api.cron.unas_translator_correcter'),
    ("0 1 * * 5", "api.cron.unas_image_upload"),
    ("0 0 * * *", "api.cron.pen_adatlap_upload"),
    ("0 0 * * *", "api.cron.fol_orders_delete_last_90"),
    ("0 0 * * *", "api.cron.sm_inventory_planner"),
    ("0 0 * * *", "api.cron.sm_auto_order"),
    ("45 * * * *", "api.cron.dataupload_retry_feed"),
]

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(os.environ.get("REDIS_HOST"), 6379), ("127.0.0.1", 6379)],
        },
    },
}
ASGI_APPLICATION = "dataupload.asgi.application"

USE_TZ = False
