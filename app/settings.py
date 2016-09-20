import os


PALOMA_HOST = os.environ.get("PALOMA", "http://localhost:5000")
IMAGE_PATH_STATIC = 'app/img/user/'
IMAGE_PATH = '{}/app/static/{}'.format(os.getcwd(), IMAGE_PATH_STATIC)
