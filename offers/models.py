from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django.utils import timezone


class Notice(models.Model):
    content = models.TextField(verbose_name='Uwagi')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'notices'


class OfferStatus(models.Model):
    offer_status = models.CharField(max_length=30, default=1)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'offer_statuses'
        verbose_name_plural = 'Offer statuses'
        ordering = ['-offer_status']

    def __str__(self):
        return self.offer_status


class Offer(models.Model):
    offer_no = models.CharField(max_length=20, verbose_name='Nr oferty')
    client = models.CharField(max_length=100, verbose_name='Klient')
    user_mark = models.ForeignKey(User,
                                  related_name='%(class)s_mark',
                                  on_delete=models.DO_NOTHING,
                                  limit_choices_to={'groups__name': 'marketing'},
                                  verbose_name='Marketingowiec',
                                  default=19,
                                  )
    user_tech = models.ForeignKey(User,
                                  related_name='%(class)s_tech',
                                  on_delete=models.DO_NOTHING,
                                  limit_choices_to={'groups__name': 'technologia'},
                                  verbose_name='Technolog',
                                  default=4,
                                  )
    date_tech_in = models.DateField(null=True, blank=True,
                                    verbose_name='Data wpływu do WZT',
                                    default=timezone.now)
    date_tech_out = models.DateField(null=True, blank=True)
    date_mark_out = models.DateField(null=True, blank=True)
    positions_amount = models.IntegerField(default=0)
    status = models.ForeignKey(OfferStatus, on_delete=models.DO_NOTHING, default=1)
    days_amount = models.IntegerField(null=True, blank=True)
    notices = models.TextField(null=True, blank=True, verbose_name='Uwagi')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'offers'

    def __str__(self):
        return '{} -- {} -- {}'.format(self.offer_no, self.client, self.positions_amount)

    @staticmethod
    def get_absolute_url():
        return reverse('offers')

    def get_days_amount(self):
        if self.status.id == 1:
            days = date.today() - self.date_tech_in
            return days.days
        return self.days_amount

    @staticmethod
    def string_from_list(attr_list):
        temp_dict = {}
        end_str = ''

        # sorting list by value
        for index, item in enumerate(attr_list, start=1):
            if item not in temp_dict:
                temp_dict[item] = [index]
            else:
                temp_dict[item].append(index)

        # making string from sorted list
        for key in temp_dict:
            end_str += '{}: '.format(key)
            for value in temp_dict[key]:
                end_str += '{},'.format(value)
            end_str += '; '

        return end_str

    def prepare_details(self):
        details = self.detail_set.all()
        machining = []
        tolerances = []
        tapers = []
        atest = []

        for detail in details:
            machining.append(detail.machining)
            tolerances.append(detail.tolerances)
            tapers.append(detail.tapers)
            atest.append(detail.atest)

        mach_str = self.string_from_list(machining)
        tol_str = self.string_from_list(tolerances)
        tap_str = self.string_from_list(tapers)
        atest_str = self.string_from_list(atest)

        return {'machining': mach_str, 'tolerances': tol_str, 'tapers': tap_str, 'atest': atest_str}


class MaterialGroup(models.Model):
    mat_group = models.IntegerField()
    description = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'material_groups'
        ordering = ['mat_group']

    def __str__(self):
        return '{} :: {}'.format(self.mat_group, self.description)


class Material(models.Model):
    material = models.CharField(max_length=100, verbose_name='Materiał')
    mat_group = models.ForeignKey(MaterialGroup, on_delete=models.SET_NULL, null=True, verbose_name='Grupa materiałowa')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'materials'
        ordering = ['material']

    def __str__(self):
        return self.material

    @staticmethod
    def get_absolute_url():
        return reverse('materials')


class HeatTreatment(models.Model):
    term = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'heat_treatments'
        ordering = ['term']

    def __str__(self):
        return self.term


class MachiningType(models.Model):
    machining = models.CharField(max_length=50, default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'machinings'
        ordering = ['machining']

    def __str__(self):
        return self.machining


class PatternTaper(models.Model):
    taper = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'pattern_tapers'

    def __str__(self):
        return self.taper


class AtestType(models.Model):
    atest = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'atest_types'

    def __str__(self):
        return self.atest


class OfferPatternStatus(models.Model):
    status = models.CharField(max_length=50, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'offer_pattern_statuses'
        verbose_name_plural = 'Offer pattern statuses'

    def __str__(self):
        return self.status


class Detail(models.Model):
    offer = models.ForeignKey(Offer, on_delete=models.DO_NOTHING)
    cast_name = models.CharField(max_length=50, blank=False, null=True, verbose_name='Nazwa odlewu')
    drawing_no = models.CharField(max_length=50, blank=False, null=True, verbose_name='Nr rysunku')
    mat = models.ForeignKey(Material, on_delete=models.DO_NOTHING, verbose_name='Materiał')
    draw_weight = models.IntegerField(blank=True, null=True, verbose_name='Ciężar rysunkowy [kg]')
    cast_weight = models.IntegerField(blank=True, null=True, verbose_name='Ciężar surowego odlewu [kg]')
    pieces_amount = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ilość sztuk', default=1)
    detail_yield = models.IntegerField(blank=True, null=True, verbose_name='Uzysk', db_column='yeld')
    difficulty = models.IntegerField(blank=True, null=True,
                                     verbose_name='Stopień trudności',
                                     default=2,
                                     choices=((1, 1), (2, 2), (3, 3))
                                     )
    pattern = models.CharField(max_length=50, blank=True, null=True, verbose_name='Model')
    heat_treat = models.CharField(max_length=50, blank=True, null=True, verbose_name='Obróbka cieplna')
    machining = models.ForeignKey(MachiningType,
                                  on_delete=models.DO_NOTHING,
                                  verbose_name='Obróbka mechaniczna',
                                  default=5)
    tolerances = models.CharField(max_length=50, blank=True, null=True, verbose_name='Tolerancje')
    tapers = models.CharField(max_length=50, blank=True, null=True, verbose_name='Pochylenia')
    atest = models.CharField(max_length=50, blank=True, null=True, verbose_name='Atest')
    required = models.CharField(max_length=50, blank=True, null=True)
    quality_class = models.CharField(max_length=50, blank=True, null=True, verbose_name='Klasa jakości')
    boxes = models.CharField(max_length=50, blank=True, null=True, verbose_name='Skrzynki formierskie')
    others = models.CharField(max_length=50, blank=True, null=True, verbose_name='Inne')
    fr_mold_work = models.FloatField(blank=True, null=True)
    fr_mold_mat = models.FloatField(blank=True, null=True)
    fr_fettling = models.FloatField(blank=True, null=True)
    fr_welding = models.FloatField(blank=True, null=True)
    fr_heating = models.FloatField(blank=True, null=True)
    fr_scrap = models.IntegerField(blank=True, null=True)
    fr_chromite = models.IntegerField(blank=True, null=True, verbose_name='Ilość chromitu [%]')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = False
        db_table = 'details'

    def __str__(self):
        return '{} {} {}'.format(self.cast_name, self.drawing_no, self.cast_weight)

    def get_absolute_url(self):
        return reverse('offer-details', kwargs={'pk': self.offer.id})
