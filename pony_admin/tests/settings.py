"""
Configuration and launcher for Pony Admin tests.
"""
import os
import tempfile

DEBUG = True
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TESTAPP_DIR = os.path.join(BASE_DIR, 'testapp/')
BLOB_DIR = os.path.join(TESTAPP_DIR, 'blobs/')

ADMIN = ('foo@bar')
ALLOWED_HOSTS = ['*']
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
)
ROOT_URLCONF = 'pony_admin.tests.urls'
SECRET_KEY = "it's a secret to everyone"
SITE_ID = 1
MEDIA_ROOT = tempfile.mkdtemp()
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pony_admin',
    'pony_admin.storage',
    # Test
    'pony_admin.tests.testapp',
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

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    "django.core.context_processors.media",
    "django.core.context_processors.static",
)
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

try:
    __import__('imp').find_module('debug_toolbar')
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE_CLASSES
    TEMPLATE_CONTEXT_PROCESSORS = ('django.template.context_processors.debug',) + TEMPLATE_CONTEXT_PROCESSORS
    # INTERNAL_IPS = os.environ.get('INTERNAL_IPS', '127.0.0.1').split(',')
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }
except ImportError:
    pass

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
            'loaders': TEMPLATE_LOADERS,
        },
    },
]
