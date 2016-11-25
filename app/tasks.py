from background_task import background
from cache import CacheSql
from app import settings
import logging
import requests
import urllib

def call_tasks(courses):
    TaskGetDolar()
    TaskCache(courses)
    #  TaskCleanCache(courses)

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

def TaskUpdateCourse(name):
    context = {
        "name": name,
        "type": 'language',
        "course": 'ingles',
    }
    url = '{}/course/detail?type={}&course={}&name={}'.format(settings.PALOMA_HOST, context['type'], context['course'], context['name'])
    response = requests.get(url)
    if response.status_code != 200:
        logging.debug("failed: status: %s " % response.status_code)
        return
    course = response.json()
    CacheSql().save(course.get("Name"), course)

@background(schedule=10)
def TaskSendRate(name, rating):
    data = {
        "name": name,
        "course": "ingles",
        "type": "language",
        "vote": str(rating)
    }
    data_qs = urllib.urlencode(data)
    url = '{}/course/feedback?{}'.format(settings.PALOMA_HOST, data_qs)
    response = requests.post(url)
    if response.status_code != 200:
        logging.debug("Failed to send feedback")
    else:
        logging.debug("Feedback ok")
        TaskUpdateCourse(name)

