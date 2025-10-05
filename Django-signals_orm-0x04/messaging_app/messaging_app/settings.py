"""Minimal settings module used to demonstrate caching configuration for the exercise.

Note: If your real Django project already has a settings.py, merge the CACHES section
from this file into your project's settings instead of replacing your settings.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Minimal settings needed for caching demonstration
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}

# Other typical settings (placeholders) — ensure your real project already defines these
INSTALLED_APPS = [
    # 'django.contrib.admin',
    # ... add your apps here
]

SECRET_KEY = "replace-this-with-real-secret"
