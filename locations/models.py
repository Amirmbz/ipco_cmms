from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

    def __str__(self):
        return f"{self.code} - {self.name}"