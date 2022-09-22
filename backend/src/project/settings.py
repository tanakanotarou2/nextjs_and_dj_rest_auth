import os
from datetime import timedelta
from pathlib import Path

from decouple import config
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = config("DJ_SECRET_KEY")

DEBUG = config("DEBUG", cast=bool, default=False)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=lambda v: [s.strip() for s in v.split(",")])

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "drf_spectacular",
    # "polls",
    "accounts",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# ==============================================================

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
# ==============================================================

STATIC_URL = "/static/"

# プロジェクトの staticファイルの配置場所
STATICFILES_DIRS = [BASE_DIR / "static"]

# collect した後に配置されるパス
STATIC_ROOT = str(BASE_DIR / "public/static/")

# media files (アップロードファイルなどが配置される場所の設定)
# ==============================================================
MEDIA_ROOT = os.path.join(BASE_DIR, "site_media/")
MEDIA_URL = "/media/"

# other django default settings
# ==============================================================

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# CORS
# ==============================================================
CORS_ORIGIN_WHITELIST = config("CORS_ORIGIN_WHITELIST", cast=lambda v: [s.strip() for s in v.split(",")])
CORS_ALLOW_CREDENTIALS = True

# REST framework
# ==============================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # page base
    # "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    # offset base
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_PARSER_CLASSES": [
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": ("djangorestframework_camel_case.render.CamelCaseJSONRenderer",),
    # doc: https://github.com/vbabiy/djangorestframework-camel-case#underscoreize-options
    "JSON_UNDERSCOREIZE": {
        "no_underscore_before_number": True,
    },
}

# dj_rest_auth
# ==============================================================

# jwt の設定
REST_USE_JWT = True
JWT_AUTH_COOKIE = "jwt-token"
JWT_AUTH_REFRESH_COOKIE = "jwt-refresh-token"
JWT_AUTH_COOKIE_USE_CSRF = True
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = config("COOKIE_SAMESITE", default="None")
JWT_AUTH_SECURE = config("COOKIE_SECURE", cast=bool, default=True)
JWT_AUTH_RETURN_EXPIRATION = True  # ログイン時のレスポンスに有効期限を含める

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=config("ACCESS_TOKEN_LIFETIME_MINUTES", cast=int, default=60)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=config("REFRESH_TOKEN_LIFETIME_DAYS", cast=int, default=30)),
    "ROTATE_REFRESH_TOKENS": True,
}

# serializer
REST_AUTH_SERIALIZERS = {
    "JWT_SERIALIZER_WITH_EXPIRATION": "prj_auth.serializers.LoginResponseSerializer",
    "USER_DETAILS_SERIALIZER": "accounts.serializers.UserDetailSerializer",
}

# CSRF トークンのクッキー設定
CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", cast=lambda v: [s.strip() for s in v.split(",")])
CSRF_COOKIE_SAMESITE = config("COOKIE_SAMESITE", default="None")
CSRF_COOKIE_SECURE = config("COOKIE_SECURE", cast=bool, default=True)

# spectacular (API document)
# https://drf-spectacular.readthedocs.io/en/latest/settings.html
# ==============================================================
SPECTACULAR_SETTINGS = {
    "SERVE_PERMISSIONS": [
        "rest_framework.permissions.AllowAny" if DEBUG else "rest_framework.permissions.IsAdminUser"
    ],
    "SWAGGER_UI_SETTINGS": {"persistAuthorization": True, "url": "http://127.0.0.1:8000/api/schema/"},
    # to camelCase
    "CAMELIZE_NAMES": True,
    "POSTPROCESSING_HOOKS": ["drf_spectacular.contrib.djangorestframework_camel_case.camelize_serializer_fields"],
    # request, response の オブジェクトを分ける. frontend で生成する create アクション(POST) の型に readonly field が含まれなくなる。
    "COMPONENT_SPLIT_REQUEST": True,
    # フロントエンドから参照するスキーマ情報には `/api/` を含めないようにしたかったため、
    # 出力するスキーマの prefix: `/api/` を除く設定をする。
    # 注) これの副作用として swagger の リクエスト先 URL も /api/ が省かれて 404 エラーとなる。
    #     swagger の設定方法がわからなかったので、env で切り替えられるようにしている。
    "SCHEMA_PATH_PREFIX_TRIM": "/api/"
    if not config("DISABLE_SCHEMA_PATH_PREFIX_TRIM", cast=bool, default=False)
    else "",
}
