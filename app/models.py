from django.db import models


class CacheModel(models.Model):
    name = models.CharField(primary_key=True, max_length=500, unique=True)
    details = models.CharField(max_length=5000)

    def __str__(self):
        return self.details
