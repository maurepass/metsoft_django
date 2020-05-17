from django.contrib.auth.models import User
from django.db import models


def get_first_name(self):
    return self.first_name


User.add_to_class("__str__", get_first_name)


class UsedViewsLogs(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    ip = models.CharField(db_column='IP', max_length=20, blank=True, null=True)
    host = models.CharField(max_length=30, blank=True, null=True)
    report = models.CharField(max_length=50, blank=True, null=True, db_column='raport')
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'logs'
