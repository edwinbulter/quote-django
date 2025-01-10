from .base import *

DEBUG = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Use a different database during tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',  # Use in-memory database for tests
    }
}
