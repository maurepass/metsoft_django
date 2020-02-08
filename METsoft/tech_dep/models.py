from datetime import date

from django.contrib.auth.models import User
from django.db import models


class OrderStatus(models.Model):
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'order_statuses'

    def __str__(self):
        return self.status


class Order(models.Model):
    id_poc = models.IntegerField(blank=True, null=True)
    numer_met = models.CharField(db_column='numer_MET', max_length=20, verbose_name='Numer zlecenia', blank=True, null=True)  # Field name made lowercase.
    company = models.CharField(max_length=200, blank=True, null=True, verbose_name='Klient')
    cast_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Nazwa odlewu')
    cast_pcs = models.IntegerField(blank=True, null=True, verbose_name='Ilość sztuk')
    pict_number = models.CharField(max_length=255, blank=True, null=True, verbose_name='Numer rysunku')
    cust_material = models.CharField(max_length=255, blank=True, null=True, verbose_name='Materiał')
    termin_klienta = models.DateField(blank=True, null=True, verbose_name='Termin klienta')
    model = models.CharField(max_length=10, blank=True, null=True, verbose_name='Model')
    rawcast = models.CharField(max_length=10, blank=True, null=True, verbose_name='Odlew')
    painting = models.CharField(max_length=10, blank=True, null=True, verbose_name='Malowanie')
    mechrough = models.CharField(max_length=10, blank=True, null=True, verbose_name='Obr. zgrubna')
    mechfine = models.CharField(max_length=10, blank=True, null=True, verbose_name='Obr. na gotowo')
    marketing = models.CharField(max_length=50, blank=True, null=True, verbose_name='Marketing')
    ord_in = models.DateField(blank=True, null=True, verbose_name='Data otrzymania')
    ord_out = models.DateField(blank=True, null=True, verbose_name='Data zakończenia')
    tech_memb = models.ForeignKey(User,
                                  on_delete=models.DO_NOTHING,
                                  limit_choices_to={'groups__name': 'technologia'},
                                  verbose_name="Technolog",
                                  blank=True, null=True
                                  )
    status = models.ForeignKey(OrderStatus,
                               on_delete=models.DO_NOTHING,
                               blank=True, null=True,
                               default=2,
                               verbose_name='Status')
    working_time = models.IntegerField(blank=True, null=True)
    important = models.IntegerField(blank=True, null=True)
    uwagi = models.CharField(max_length=100, blank=True, null=True, verbose_name='Uwagi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'orders'

    def __str__(self):
        return '{} {} {} {} {}'.format(self.numer_met, self.company, self.cast_name, self.tech_memb, self.status)

    def get_working_time(self):
        if self.status.id == 2:
            days = date.today() - self.ord_in
            return days.days
        return self.working_time
