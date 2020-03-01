from datetime import timedelta, date

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_extensions.management.jobs import DailyJob

from METsoft.settings import EMAIL_HOST_USER
from offers.models import Offer
from prod_reports.models import Operation
from tech_dep.models import Order


class Job(DailyJob):
    """ Send mail with offers and orders in progress and nonconformities from last day"""

    def execute(self):
        # if is Monday send nonconformities since Friday
        if date.isoweekday(date.today()) == 1:
            completion_date = date.today() - timedelta(days=3)
        else:
            completion_date = date.today() - timedelta(days=1)

        context = {
            'offers': Offer.objects.filter(status_id=1).order_by('-id'),
            'orders': Order.objects.filter(status_id=2).order_by('-id'),
            'nonconformities': Operation.objects.filter(accordance=3, completion_date1=completion_date)
        }

        users = User.objects.filter(groups__name='raport')

        send_mail('METsoft - daily mail',
                  'Some message',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email for user in users],
                  html_message=render_to_string('tech_dep/daily_mail_tech_department.html', context)
                  )
