from django.core.mail import send_mail

from .models import Notification


def notify_users(users, notif_type, message, work_order=None):
    for user in users:
        Notification.objects.create(user=user, type=notif_type, message=message, work_order=work_order)
        if user.email:
            send_mail(subject=notif_type, message=message, from_email=None, recipient_list=[user.email])