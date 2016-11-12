import redis
import json
from urlparse import urlparse

from app import settings
from app.models import CacheModel

class CacheSql():
    def _save(self, key, value):
        try:
            if CacheModel.objects.filter(name=str(key)).exists():
                CacheModel.objects.filter(name=str(key)).delete()
            object = CacheModel.objects.create(
                name=str(key),
                details=json.dumps(value)
            )
            object.save()
        except Exception as error:
            print "Don't save because: %s" % error

    def save(self, courses):
        for course in courses:
            self._save(course.get("Name"), course)

    def delete(self, key):
        try:
            CacheModel.objects.filter(name=str(key)).delete()
        except Exception as error:
            print "Don't remove because: %s" % error

    def get(self, key):
        try:
            if not CacheModel.objects.filter(name=str(key)).exists():
                raise KeyError('invalid')
            value = CacheModel.objects.get(name=str(key)).__str__()
            return json.loads(value)
        except Exception as error:
            raise error

