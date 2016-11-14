from background_task import background
from cache import CacheSql
from app import settings
import logging
import requests


@background(schedule=6)
def TaskCache(courses):
    logging.debug("saving courses: ")
    for course in courses:
        logging.debug("saving course: %s" % course.get("Name"))
        CacheSql().save(course.get("Name"), course)
    logging.debug("saving questions: ")
    url = '{}/courses/questions?type={}'.format(settings.PALOMA_HOST, 'language')
    response = requests.get(url)
    if response.status_code != 200:
        logging.debug("Failed get questions")
    questions = response.json()
    CacheSql().save("Questions", questions)

