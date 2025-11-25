from django.contrib.auth.models import User
from django.db import models


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=100)
    message = models.TextField()
    work_order = models.ForeignKey('work_orders.WorkOrder', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} - {self.user}"