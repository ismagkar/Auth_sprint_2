import os

DATABASES = {
    "default": {
        "ENGINE": os.environ.get("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", default="127.0.0.1"),
        "PORT": os.environ.get("DB_PORT", default=5432),
        "OPTIONS": {"options": "-c search_path=public,content"},
    },
}
