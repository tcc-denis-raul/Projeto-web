import redis
import json
from urlparse import urlparse

from app import settings


class Cache():
    def __init__(self):
        self.host = urlparse(settings.REDIS_HOST)
        self.client = redis.StrictRedis(host=self.host.hostname, port=self.host.port)
        self.HASH = "courses"

    def _save(self, key, value):
        try:
            if self.client.hexists(self.HASH, key):
                self.client.expire(self.HASH, 300)
            self.client.hset(self.HASH, key, json.dumps(value))
            self.client.expire(self.HASH, 300)
        except Exception as error:
            print "Dont save because: %s" % error

    def save(self, courses):
        for course in courses:
            self._save(course.get("Name"), course)

    def get(self, key):
        if not self.client.hexists(self.HASH, key):
            raise KeyError('invalid')
        value = self.client.hget(self.HASH, key)
        return json.loads(value)
