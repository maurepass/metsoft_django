from datetime import date

from django.db import models
from django.urls import reverse


class PatternStatus(models.Model):
    status = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'pattern_statuses'
        verbose_name_plural = 'PatternStatuses'

    def __str__(self):
        return self.status


class Pattern(models.Model):
    customer = models.CharField('Nazwa firmy', max_length=100, blank=True, null=True)
    drawing_number = models.CharField('Numer rysunku', max_length=100, blank=True, null=True)
    pattern_name = models.CharField('Nazwa odlewu', max_length=100, blank=True, null=True)
    last_order = models.DateField('Ostatnie zlecenie', blank=True, null=True, default=date.today)
    orders_amount = models.IntegerField('Ilość zleceń', blank=True, null=True, default=1)
    area = models.FloatField('Powierzchnia', blank=True, null=True)
    layer_number = models.CharField('Numer ułożenia', max_length=100, blank=True, null=True)
    layer_place = models.CharField('Miejsce ułożenia', max_length=100, blank=True, null=True)
    material = models.CharField('Materiał', max_length=30, blank=True, null=True)
    cart_number = models.CharField('Numer kartoteki', max_length=30, blank=True, null=True)
    pattern_index = models.CharField('Numer indexu modelu', max_length=100, blank=True, null=True)
    verification = models.TextField('Weryfikacja', blank=True, null=True)
    remarks = models.TextField('Uwagi', blank=True, null=True)
    verification_date = models.CharField(
        'Data weryfikacji',
        max_length=30,
        blank=True,
        null=True,
        default=date.today
    )
    surname = models.CharField('Nazwisko', max_length=100, blank=True, null=True)
    status = models.ForeignKey(
        PatternStatus,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='status',
        default=1
    )
    move_in = models.DateField(
        'Data zmiany statusu',
        blank=True,
        null=True,
        default=date.today
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        db_table = 'patterns'

    def __str__(self):
        return '{}'.format(self.pattern_name)

    @staticmethod
    def get_absolute_url():
        return reverse('patterns:patterns')

    def get_not_using_time(self):
        if self.status.id in [4, 5, 6, 7]:
            return None
        if self.last_order:
            diff = date.today() - self.last_order
            return int(diff.days/30)
        return None


class PatternHistory(models.Model):
    pattern = models.ForeignKey(Pattern, on_delete=models.CASCADE, default=1)
    status = models.ForeignKey(PatternStatus, on_delete=models.DO_NOTHING, default=1)
    date = models.DateField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'pattern_history'
        verbose_name_plural = 'PatternHistory'
