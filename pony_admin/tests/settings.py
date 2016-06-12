"""
Configuration and launcher for Pony Admin tests.
"""
import os
import tempfile


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTAPP_DIR = os.path.join(BASE_DIR, 'testapp/')
BLOB_DIR = os.path.join(TESTAPP_DIR, 'blobs/')

ADMIN = ('foo@bar')
ALLOWED_HOSTS = ['*']
MIDDLEWARE_CLASSES = ()
ROOT_URLCONF = 'pony_admin.tests.urls'
SECRET_KEY = "it's a secret to everyone"
SITE_ID = 1
MEDIA_ROOT = tempfile.mkdtemp()
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'pony_admin',
    'pony_admin.storage',
)

try:
    import dj_database_url
    DATABASE = dj_database_url.config(default='sqlite:///%s' %
                                      tempfile.mktemp())
    DATABASES = {'default': DATABASE}
except ImportError:
    DATABASES = {
        'default': {
            'NAME': tempfile.mktemp(),
            'ENGINE': 'django.db.backends.sqlite3'
        }
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = tempfile.mkdtemp()
