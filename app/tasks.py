from background_task import background
from cache import CacheSql
from app import settings
import logging
import requests

def call_tasks(courses):
    TaskGetDolar()
    TaskCache(courses)
    TaskCleanCache(courses)

@background(schedule=10)
def TaskGetDolar():
    response = requests.get("http://dolarhoje.com/cotacao.txt")
    if response.status_code != 200:
        logging.debug("Wrong in obtain dolar")
        dolar = 3.4
    else:
        dolar = response.text.replace(',', '.')
    CacheSql().save("Dolar", dolar)

@background(schedule=60*60)
def TaskCleanCache(courses):
    logging.debug("Clean cache: ")
    for course in courses:
        logging.debug("clean course: %s" % course.get("Name"))
        CacheSql().delete(course.get("Name"))
    logging.debug("Clean questions: ")
    CacheSql().delete("Questions")

@background(schedule=10)
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

