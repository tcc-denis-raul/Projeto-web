from django.db import models


class CacheModel(models.Model):
    name = models.CharField(max_length=100, unique=True)
    data = models.CharField(max_length=500)

    def __str__(self):
        return self.data
