import datetime

from django.db import connections, models
from django.db.models import Count, F, Max, Q, Sum


class Customer(models.Model):
    company = models.CharField(unique=True, max_length=128)
    companyshort = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    surname = models.CharField(max_length=64)
    added_date = models.DateTimeField()
    added_by = models.CharField(max_length=32)
    active = models.IntegerField()
    status = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    address = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class User(models.Model):
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirmation_code = models.CharField(max_length=255)
    remember_token = models.CharField(max_length=255, blank=True, null=True)
    confirmed = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'


class Material(models.Model):
    materialname = models.CharField(max_length=50)
    calcgroup = models.CharField(max_length=5)
    qc = models.DecimalField(db_column='qC', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qsi = models.DecimalField(db_column='qSi', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qmn = models.DecimalField(db_column='qMn', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp = models.DecimalField(db_column='qP', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qs = models.DecimalField(db_column='qS', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qcr = models.DecimalField(db_column='qCr', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qmo = models.DecimalField(db_column='qMo', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qni = models.DecimalField(db_column='qNi', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qal = models.DecimalField(db_column='qAl', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp1 = models.DecimalField(db_column='qP1', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp2 = models.DecimalField(db_column='qP2', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp3 = models.DecimalField(db_column='qP3', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp4 = models.DecimalField(db_column='qP4', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp5 = models.DecimalField(db_column='qP5', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    np1 = models.DecimalField(db_column='nP1', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    np2 = models.DecimalField(db_column='nP2', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    np3 = models.DecimalField(db_column='nP3', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    np4 = models.DecimalField(db_column='nP4', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    np5 = models.DecimalField(db_column='nP5', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qcmin = models.DecimalField(db_column='qCmin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qcmax = models.DecimalField(db_column='qCmax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qsimin = models.DecimalField(db_column='qSimin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qsimax = models.DecimalField(db_column='qSimax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qmnmin = models.DecimalField(db_column='qMnmin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qmnmax = models.DecimalField(db_column='qMnmax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qpmin = models.DecimalField(db_column='qPmin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qpmax = models.DecimalField(db_column='qPmax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qsmin = models.DecimalField(db_column='qSmin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qsmax = models.DecimalField(db_column='qSmax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qcrmin = models.DecimalField(db_column='qCrmin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qcrmax = models.DecimalField(db_column='qCrmax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qmomin = models.DecimalField(db_column='qMomin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qmomax = models.DecimalField(db_column='qMomax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qnimin = models.DecimalField(db_column='qNimin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qnimax = models.DecimalField(db_column='qNimax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qalmin = models.DecimalField(db_column='qAlmin', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qalmax = models.DecimalField(db_column='qAlmax', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp1min = models.DecimalField(db_column='qP1min', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp1max = models.DecimalField(db_column='qP1max', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp2min = models.DecimalField(db_column='qP2min', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp2max = models.DecimalField(db_column='qP2max', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp3min = models.DecimalField(db_column='qP3min', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp3max = models.DecimalField(db_column='qP3max', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp4min = models.DecimalField(db_column='qP4min', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp4max = models.DecimalField(db_column='qP4max', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp5min = models.DecimalField(db_column='qP5min', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    qp5max = models.DecimalField(db_column='qP5max', max_digits=10, decimal_places=3, blank=True, null=True)  # Field name made lowercase.
    updated_at = models.DateField(blank=True, null=True)
    created_at = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'materials'


class Porder(models.Model):
    opis_zlecenia = models.CharField(max_length=128)
    numer_oferty = models.CharField(max_length=32)
    met_no = models.CharField(db_column='numer_MET', max_length=16)  # Field name made lowercase.
    data_zamowienia = models.DateField(blank=True, null=True)
    zamawiajacy = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, db_column='zamawiajacy')
    nr_zamowienia = models.CharField(max_length=32)
    customer_date = models.DateField(blank=True, null=True, db_column='termin_klienta')
    termin_realizacji = models.DateField(blank=True, null=True)
    wprowadzajacy = models.CharField(max_length=20, db_column='wprowadzajacy_id')
    data_przekwzt = models.DateField(blank=True, null=True)
    data_wplywu_do_pzm = models.DateField(blank=True, null=True)
    kontrolka_tech = models.DateField(blank=True, null=True)
    kontrolka_plan = models.DateField(blank=True, null=True)
    kontrolka_dkj = models.DateField(blank=True, null=True)
    kontrolka_sp = models.DateField(blank=True, null=True)
    prowadzacy_pzm = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_column='prowadzacy_pzm')
    data_wplywu_zlec_do_pzm = models.DateField(blank=True, null=True)
    uwagi = models.TextField(blank=True, null=True)
    aktywny = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    rodzaj = models.IntegerField(blank=True, null=True)
    data_potw_zam = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'porders'


class Pocastord(models.Model):
    porder = models.ForeignKey(Porder, on_delete=models.DO_NOTHING, db_column='id_po')
    id_tech = models.IntegerField(blank=True, null=True)
    cast_name = models.CharField(max_length=64)
    cast_pcs = models.IntegerField()
    material = models.CharField(max_length=64, blank=True, null=True)
    cust_material = models.CharField(max_length=64)
    pict_number = models.CharField(max_length=64)
    model = models.IntegerField(blank=True, null=True)
    rawcast = models.IntegerField(blank=True, null=True)
    thermal = models.IntegerField(blank=True, null=True)
    painting = models.IntegerField(blank=True, null=True)
    mechrough = models.IntegerField(blank=True, null=True)
    mechfine = models.IntegerField(blank=True, null=True)
    castprice = models.FloatField(blank=True, null=True)
    castworth = models.FloatField(blank=True, null=True)
    other = models.TextField(blank=True, null=True)
    aktywny = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    total_weight = models.FloatField(blank=True, null=True)
    planned_pcs = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pocastords'

    def __str__(self):
        return '{} {} {}'.format(self.cast_name, self.cast_pcs, self.cust_material)


class Cast(models.Model):
    porder = models.ForeignKey(
        Porder,
        db_column='id_po',
        on_delete=models.DO_NOTHING
    )
    cast_name = models.CharField(max_length=64, blank=True, null=True)
    tech = models.ForeignKey(
        User,
        blank=True,
        null=True,
        db_column='id_tech',
        on_delete=models.DO_NOTHING
    )
    picture_number = models.CharField(max_length=64, blank=True, null=True)
    pc_number = models.IntegerField(blank=True, null=True)
    cast_tries = models.IntegerField(blank=True, null=True)
    trash_tries = models.IntegerField(blank=True, null=True)
    mat_calc_group = models.CharField(max_length=8, blank=True, null=True)
    cast_type = models.IntegerField(blank=True, null=True)
    model_customer = models.IntegerField(blank=True, null=True)
    model_warehouse = models.IntegerField(blank=True, null=True)
    model_new = models.IntegerField(blank=True, null=True)
    model_refactor = models.IntegerField(blank=True, null=True)
    model_repair = models.IntegerField(blank=True, null=True)
    dim_tolerance = models.CharField(max_length=32, blank=True, null=True)
    cast_slope = models.IntegerField(blank=True, null=True)
    marking_method = models.CharField(max_length=64, blank=True, null=True)
    thermal = models.CharField(max_length=64, blank=True, null=True)
    mech_proc_status = models.IntegerField(blank=True, null=True)
    painting_cover = models.CharField(max_length=255, blank=True, null=True)
    other_receipt = models.CharField(max_length=255, blank=True, null=True)
    creation_date = models.DateField(blank=True, null=True)
    documentation_issue_date = models.DateField(blank=True, null=True)
    final_receipt_date = models.DateField(blank=True, null=True)
    trial_pcs = models.IntegerField(blank=True, null=True)
    tech_maker = models.CharField(max_length=64, blank=True, null=True)
    tech_generate = models.CharField(max_length=64, blank=True, null=True)
    customer = models.CharField(max_length=128, blank=True, null=True)
    order_number = models.CharField(max_length=32, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    customer_material = models.CharField(max_length=32, blank=True, null=True)
    cast_material = models.ForeignKey(
        Material,
        on_delete=models.DO_NOTHING,
        db_column='cast_material'
    )
    cast_weight = models.FloatField(blank=True, null=True)
    material_need = models.IntegerField(blank=True, null=True)
    mould_start_mintemp = models.IntegerField(blank=True, null=True)
    mould_start_maxtemp = models.IntegerField(blank=True, null=True)
    cast_cooling_time = models.IntegerField(blank=True, null=True)
    electrode_type = models.CharField(max_length=64, blank=True, null=True)
    other_customer_needs = models.TextField(blank=True, null=True)
    atest_chem = models.CharField(max_length=64, blank=True, null=True)
    atest_mech = models.CharField(max_length=64, blank=True, null=True)
    atest_hard = models.CharField(max_length=64, blank=True, null=True)
    atest_other_mat_need = models.CharField(max_length=256, blank=True, null=True)
    tests_ut = models.CharField(max_length=32, blank=True, null=True)
    tests_mt = models.CharField(max_length=32, blank=True, null=True)
    tests_pt = models.CharField(max_length=32, blank=True, null=True)
    tests_rt = models.CharField(max_length=32, blank=True, null=True)
    tests_vt = models.CharField(max_length=32, blank=True, null=True)
    tests_other = models.CharField(max_length=64, blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    cast_status = models.IntegerField(blank=True, null=True)
    cast_clones_from_po = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    melt = models.IntegerField(blank=True, null=True)
    pocastord = models.ForeignKey(
        Pocastord,
        on_delete=models.DO_NOTHING,
        db_column='id_poc',
        blank=True,
        null=True
    )
    pplan_id = models.IntegerField()
    pplansposition_id = models.IntegerField(blank=True, null=True)
    delivery_id = models.IntegerField(blank=True, null=True)
    is_outgroup = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'casts'

    @staticmethod
    def monitoring():
        objects = (
            Cast.objects
            .values('pocastord__id')
            .annotate(
                met_no=Max('porder__met_no'),
                customer=Max('customer'),
                cast_name=Max('cast_name'),
                picture_number=Max('picture_number'),
                cast_mat=Max('cast_material__materialname'),
                casting_weight=Max('cast_weight'),
                tech_maker=Max('tech_maker'),
                customer_date=Max('porder__customer_date'),
                cast_pcs=Max('pocastord__cast_pcs'),
                new=Count('cast_weight', filter=Q(cast_status=1)),
                planned=Count('cast_weight', filter=Q(cast_status=7)),
                poured=Count('cast_weight', filter=Q(cast_status=2)),
                finished=Count('cast_weight', filter=Q(cast_status=3)),
                sent=Count('cast_weight', filter=Q(cast_status=6)),
                scraped=Count('cast_weight', filter=Q(cast_status=5)),
                cancelled=Count('cast_weight', filter=Q(cast_status=4)),
            )
            .order_by('-pocastord__id')
        )
        return objects


class OperationDict(models.Model):
    operationname = models.CharField(max_length=64)
    parameter_type1 = models.CharField(max_length=64)
    parameter_type2 = models.CharField(max_length=64)
    parameter_type3 = models.CharField(max_length=64)
    parameter_type4 = models.CharField(max_length=64)
    parameter_type5 = models.CharField(max_length=64)
    defaultop = models.IntegerField()
    defaultop_weight = models.IntegerField()
    notes = models.TextField()
    active = models.IntegerField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'operation_dicts'


class AccordanceDict(models.Model):
    accname = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = 'accordance_dicts'


class Operation(models.Model):
    cast = models.ForeignKey(Cast, db_column='id_cast', on_delete=models.DO_NOTHING)
    opdict = models.ForeignKey(OperationDict, db_column='id_opdict', on_delete=models.DO_NOTHING)
    parameter_type1 = models.CharField(max_length=64, blank=True, null=True)
    parameter_value1 = models.CharField(max_length=64, blank=True, null=True)
    parameter_type2 = models.CharField(max_length=64, blank=True, null=True)
    parameter_value2 = models.CharField(max_length=64, blank=True, null=True)
    parameter_type3 = models.CharField(max_length=64, blank=True, null=True)
    parameter_value3 = models.CharField(max_length=64, blank=True, null=True)
    parameter_type4 = models.CharField(max_length=64, blank=True, null=True)
    parameter_value4 = models.CharField(max_length=64, blank=True, null=True)
    parameter_type5 = models.CharField(max_length=64, blank=True, null=True)
    parameter_value5 = models.CharField(max_length=64, blank=True, null=True)
    required = models.IntegerField(blank=True, null=True)
    accordance = models.ForeignKey(AccordanceDict, on_delete=models.DO_NOTHING, db_column='accordance')
    planned_date = models.DateField(blank=True, null=True)
    added_by = models.CharField(max_length=64, blank=True, null=True)
    innaccordance_dec = models.CharField(max_length=128, blank=True, null=True)
    complete = models.IntegerField(blank=True, null=True)
    completion_date1 = models.DateField(blank=True, null=True)
    confirmed_by1 = models.CharField(max_length=64, blank=True, null=True)
    completion_date2 = models.DateField(blank=True, null=True)
    confirmed_by2 = models.CharField(max_length=64, blank=True, null=True)
    completion_date3 = models.DateField(blank=True, null=True)
    confirmed_by3 = models.CharField(max_length=64, blank=True, null=True)
    completion_date4 = models.DateField(blank=True, null=True)
    confirmed_by4 = models.CharField(max_length=64, blank=True, null=True)
    completion_date5 = models.DateField(blank=True, null=True)
    confirmed_by5 = models.CharField(max_length=64, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    status = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    innaccordance_dec1 = models.CharField(max_length=128, blank=True, null=True)
    innaccordance_dec2 = models.CharField(max_length=128, blank=True, null=True)
    innaccordance_dec3 = models.CharField(max_length=128, blank=True, null=True)
    innaccordance_dec4 = models.CharField(max_length=128, blank=True, null=True)
    innaccordance_dec5 = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operations'
