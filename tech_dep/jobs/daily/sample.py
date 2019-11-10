from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_extensions.management.jobs import DailyJob


from METsoft.settings import EMAIL_HOST_USER
from offers.models import Offer
from tech_dep.models import Order


class Job(DailyJob):
    """ Send mail with offers and orders in progress. """

    def execute(self):
        context = {
            'offers': Offer.objects.filter(status_id=1).order_by('-id'),
            'orders': Order.objects.filter(status_id=2).order_by('-id'),
        }

        user = User.objects.get(pk=4)

        send_mail('METsoft - daily mail',
                  'Some message',
                  from_email=EMAIL_HOST_USER,
                  recipient_list=[user.email],
                  html_message=render_to_string('tech_dep/daily_mail_tech_department.html', context)
                  )
