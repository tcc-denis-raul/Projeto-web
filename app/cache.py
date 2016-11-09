import json

from app import settings
from app.models import CacheModel

class Cache():
    def _save(self, key, value):
        try:
            if CacheModel.objects.filter(name=value).exists():
                CacheModel.objects.exclude(name=value)
            value = CacheModel.objects.create(name=value, data=json.dumps(value))
            value.save()
        except Exception as error:
            print "Dont save because: {}, {}, {}".format(
                error, key, value
            )

    def save(self, courses):
        for course in courses:
            self._save(course.get("Name"), course)

    def get(self, key):
        try:
            value = self.client.hget(self.HASH, key)
        except Exception:
            raise Exception
