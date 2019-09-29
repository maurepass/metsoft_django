import socket

from django.contrib.auth.models import User
from django.db import models


def get_first_name(self):
    return self.first_name


User.add_to_class("__str__", get_first_name)


class UsedViewsLogs(models.Model):
    ip = models.CharField(max_length=20)
    host = models.CharField(max_length=30)
    report = models.CharField(max_length=50, db_column='raport')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'logs'
