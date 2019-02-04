from __future__ import absolute_import, unicode_literals
from .common import *

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = True
ALLOWED_HOSTS = ['*']

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = 'krr%0&fl+!rd^f!6k&8mxf&as98d7as9a87(*&d-as09_S)AD9'

# DJANGO DEBUG TOOLBAR
# ------------------------------------------------------------------------------
INSTALLED_APPS  = ['debug_toolbar',] + INSTALLED_APPS
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE

INTERNAL_IPS = ('127.0.0.1',)