import os


PALOMA_HOST = os.environ.get("PALOMA", "http://localhost:5000")
REDIS_HOST = os.environ.get("REDIS_URL", "http://localhost:6379")

USER_IMAGE_STATIC = 'app/img/user/'
USER_IMAGE_PATH_COMPLETE = '{}/app/static/{}'.format(os.getcwd(), USER_IMAGE_STATIC)

TYPES_IMAGE_STATIC = 'app/img/types/'
TYPES_IMAGE_PATH_COMPLETE = '{}/app/static/{}'.format(os.getcwd, TYPES_IMAGE_STATIC)

LOGO_IMAGE_STATIC = 'app/img/logos/'
LOGO_IMAGE_PATH_COMPLETE = '{}/app/static/{}'.format(os.getcwd, LOGO_IMAGE_STATIC)
