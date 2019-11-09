from django_extensions.management.jobs import DailyJob

from tech_dep.views import daily_mail_tech_department


class Job(DailyJob):

    def execute(self):
        daily_mail_tech_department()
