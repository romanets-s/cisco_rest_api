import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

MEDIA_ROOT = (
    BASE_DIR
)

MEDIA_URL = '/media/'

DEBUG = True
