from django.db import models


class Plant(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.code} - {self.name}"