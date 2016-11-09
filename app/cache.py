import redis
import json
from urlparse import urlparse

from app import settings


class Cache():
    def __init__(self):
        self.host = urlparse(settings.REDIS_HOST)
        self.client = redis.StrictRedis(
            host=self.host.hostname,
            port=int(self.host.port),
            password=settings.REDIS_PWD
        )
        self.HASH = "courses"

    def _save(self, key, value):
        try:
            if self.client.hexists(self.HASH, key):
                self.client.expire(self.HASH, 300)
            print "key: %s" % key
            print "value: %s" % json.dumps(value)
            self.client.hset(self.HASH, key, json.dumps(value))
            self.client.expire(self.HASH, 300)
        except Exception as error:
            print "Dont save because: {}, {}, {}".format(
                error, key, value
            )

    def save(self, courses):
        for course in courses:
            self._save(course.get("Name"), course)

    def get(self, key):
        try:
            if not self.client.hexists(self.HASH, key):
                raise KeyError('invalid')
            value = self.client.hget(self.HASH, key)
            return json.loads(value)
        except Exception:
            raise Exception
