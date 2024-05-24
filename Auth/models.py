from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from datetime import datetime


def upload_to(instance, filename):
    return 'profile/{filename}'.format(filename=filename)

class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_vendor = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=False)
    acc_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    phone_num = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(_("Image"), upload_to=upload_to, null=True, blank=True)


class Message(models.Model):
    room = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, limit_choices_to={'is_client': True})
    sender = models.CharField(max_length=1000000, blank=True, null=True)
    message = models.CharField(max_length=1000000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{str(self.room.username)} - {self.sender}"