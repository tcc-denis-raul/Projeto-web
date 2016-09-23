import os


PALOMA_HOST = os.environ.get("PALOMA", "http://localhost:5000")

USER_IMAGE_STATIC = 'app/img/user/'
USER_IMAGE_PATH_COMPLETE = '{}/app/static/{}'.format(os.getcwd(), USER_IMAGE_STATIC)

TYPES_IMAGE_STATIC = 'app/img/types/'
TYPES_IMAGE_PATH_COMPLETE = '{}/app/static/{}'.format(os.getcwd, TYPES_IMAGE_STATIC)

LOGO_IMAGE_STATIC = 'app/img/logo/'
LOGO_IMAGE_PATH_COMPLETE = '{}/app/static/{}'.format(os.getcwd, LOGO_IMAGE_STATIC)
