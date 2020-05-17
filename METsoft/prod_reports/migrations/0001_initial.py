# Generated by Django 2.2.10 on 2020-05-17 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AccordanceDict",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("accname", models.CharField(max_length=16)),
            ],
            options={"db_table": "accordance_dicts", "managed": False,},
        ),
        migrations.CreateModel(
            name="Cast",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("cast_name", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "picture_number",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("pc_number", models.IntegerField(blank=True, null=True)),
                ("cast_tries", models.IntegerField(blank=True, null=True)),
                ("trash_tries", models.IntegerField(blank=True, null=True)),
                (
                    "mat_calc_group",
                    models.CharField(blank=True, max_length=8, null=True),
                ),
                ("cast_type", models.IntegerField(blank=True, null=True)),
                ("model_customer", models.IntegerField(blank=True, null=True)),
                ("model_warehouse", models.IntegerField(blank=True, null=True)),
                ("model_new", models.IntegerField(blank=True, null=True)),
                ("model_refactor", models.IntegerField(blank=True, null=True)),
                ("model_repair", models.IntegerField(blank=True, null=True)),
                (
                    "dim_tolerance",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                ("cast_slope", models.IntegerField(blank=True, null=True)),
                (
                    "marking_method",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("thermal", models.CharField(blank=True, max_length=64, null=True)),
                ("mech_proc_status", models.IntegerField(blank=True, null=True)),
                (
                    "painting_cover",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "other_receipt",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("creation_date", models.DateField(blank=True, null=True)),
                ("documentation_issue_date", models.DateField(blank=True, null=True)),
                ("final_receipt_date", models.DateField(blank=True, null=True)),
                ("trial_pcs", models.IntegerField(blank=True, null=True)),
                ("tech_maker", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "tech_generate",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("customer", models.CharField(blank=True, max_length=128, null=True)),
                (
                    "order_number",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                (
                    "customer_material",
                    models.CharField(blank=True, max_length=32, null=True),
                ),
                ("cast_weight", models.FloatField(blank=True, null=True)),
                ("material_need", models.IntegerField(blank=True, null=True)),
                ("mould_start_mintemp", models.IntegerField(blank=True, null=True)),
                ("mould_start_maxtemp", models.IntegerField(blank=True, null=True)),
                ("cast_cooling_time", models.IntegerField(blank=True, null=True)),
                (
                    "electrode_type",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("other_customer_needs", models.TextField(blank=True, null=True)),
                ("atest_chem", models.CharField(blank=True, max_length=64, null=True)),
                ("atest_mech", models.CharField(blank=True, max_length=64, null=True)),
                ("atest_hard", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "atest_other_mat_need",
                    models.CharField(blank=True, max_length=256, null=True),
                ),
                ("tests_ut", models.CharField(blank=True, max_length=32, null=True)),
                ("tests_mt", models.CharField(blank=True, max_length=32, null=True)),
                ("tests_pt", models.CharField(blank=True, max_length=32, null=True)),
                ("tests_rt", models.CharField(blank=True, max_length=32, null=True)),
                ("tests_vt", models.CharField(blank=True, max_length=32, null=True)),
                ("tests_other", models.CharField(blank=True, max_length=64, null=True)),
                ("active", models.IntegerField(blank=True, null=True)),
                ("cast_clones_from_po", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("melt", models.IntegerField(blank=True, null=True)),
                ("pplan_id", models.IntegerField()),
                ("pplansposition_id", models.IntegerField(blank=True, null=True)),
                ("delivery_id", models.IntegerField(blank=True, null=True)),
                ("is_outgroup", models.IntegerField()),
            ],
            options={"db_table": "casts", "managed": False,},
        ),
        migrations.CreateModel(
            name="CastStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("statusname", models.CharField(max_length=50)),
            ],
            options={"db_table": "caststatuses", "managed": False,},
        ),
        migrations.CreateModel(
            name="Customer",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("company", models.CharField(max_length=128, unique=True)),
                ("companyshort", models.CharField(max_length=64)),
                ("name", models.CharField(max_length=64)),
                ("surname", models.CharField(max_length=64)),
                ("added_date", models.DateTimeField()),
                ("added_by", models.CharField(max_length=32)),
                ("active", models.IntegerField()),
                ("status", models.IntegerField()),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={"db_table": "customers", "managed": False,},
        ),
        migrations.CreateModel(
            name="Material",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("materialname", models.CharField(max_length=50)),
                ("calcgroup", models.CharField(max_length=5)),
                (
                    "qc",
                    models.DecimalField(
                        blank=True,
                        db_column="qC",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qsi",
                    models.DecimalField(
                        blank=True,
                        db_column="qSi",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qmn",
                    models.DecimalField(
                        blank=True,
                        db_column="qMn",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp",
                    models.DecimalField(
                        blank=True,
                        db_column="qP",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qs",
                    models.DecimalField(
                        blank=True,
                        db_column="qS",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qcr",
                    models.DecimalField(
                        blank=True,
                        db_column="qCr",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qmo",
                    models.DecimalField(
                        blank=True,
                        db_column="qMo",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qni",
                    models.DecimalField(
                        blank=True,
                        db_column="qNi",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qal",
                    models.DecimalField(
                        blank=True,
                        db_column="qAl",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp1",
                    models.DecimalField(
                        blank=True,
                        db_column="qP1",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp2",
                    models.DecimalField(
                        blank=True,
                        db_column="qP2",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp3",
                    models.DecimalField(
                        blank=True,
                        db_column="qP3",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp4",
                    models.DecimalField(
                        blank=True,
                        db_column="qP4",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp5",
                    models.DecimalField(
                        blank=True,
                        db_column="qP5",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "np1",
                    models.DecimalField(
                        blank=True,
                        db_column="nP1",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "np2",
                    models.DecimalField(
                        blank=True,
                        db_column="nP2",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "np3",
                    models.DecimalField(
                        blank=True,
                        db_column="nP3",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "np4",
                    models.DecimalField(
                        blank=True,
                        db_column="nP4",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "np5",
                    models.DecimalField(
                        blank=True,
                        db_column="nP5",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qcmin",
                    models.DecimalField(
                        blank=True,
                        db_column="qCmin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qcmax",
                    models.DecimalField(
                        blank=True,
                        db_column="qCmax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qsimin",
                    models.DecimalField(
                        blank=True,
                        db_column="qSimin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qsimax",
                    models.DecimalField(
                        blank=True,
                        db_column="qSimax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qmnmin",
                    models.DecimalField(
                        blank=True,
                        db_column="qMnmin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qmnmax",
                    models.DecimalField(
                        blank=True,
                        db_column="qMnmax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qpmin",
                    models.DecimalField(
                        blank=True,
                        db_column="qPmin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qpmax",
                    models.DecimalField(
                        blank=True,
                        db_column="qPmax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qsmin",
                    models.DecimalField(
                        blank=True,
                        db_column="qSmin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qsmax",
                    models.DecimalField(
                        blank=True,
                        db_column="qSmax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qcrmin",
                    models.DecimalField(
                        blank=True,
                        db_column="qCrmin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qcrmax",
                    models.DecimalField(
                        blank=True,
                        db_column="qCrmax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qmomin",
                    models.DecimalField(
                        blank=True,
                        db_column="qMomin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qmomax",
                    models.DecimalField(
                        blank=True,
                        db_column="qMomax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qnimin",
                    models.DecimalField(
                        blank=True,
                        db_column="qNimin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qnimax",
                    models.DecimalField(
                        blank=True,
                        db_column="qNimax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qalmin",
                    models.DecimalField(
                        blank=True,
                        db_column="qAlmin",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qalmax",
                    models.DecimalField(
                        blank=True,
                        db_column="qAlmax",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp1min",
                    models.DecimalField(
                        blank=True,
                        db_column="qP1min",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp1max",
                    models.DecimalField(
                        blank=True,
                        db_column="qP1max",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp2min",
                    models.DecimalField(
                        blank=True,
                        db_column="qP2min",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp2max",
                    models.DecimalField(
                        blank=True,
                        db_column="qP2max",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp3min",
                    models.DecimalField(
                        blank=True,
                        db_column="qP3min",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp3max",
                    models.DecimalField(
                        blank=True,
                        db_column="qP3max",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp4min",
                    models.DecimalField(
                        blank=True,
                        db_column="qP4min",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp4max",
                    models.DecimalField(
                        blank=True,
                        db_column="qP4max",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp5min",
                    models.DecimalField(
                        blank=True,
                        db_column="qP5min",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                (
                    "qp5max",
                    models.DecimalField(
                        blank=True,
                        db_column="qP5max",
                        decimal_places=3,
                        max_digits=10,
                        null=True,
                    ),
                ),
                ("updated_at", models.DateField(blank=True, null=True)),
                ("created_at", models.DateField(blank=True, null=True)),
            ],
            options={"db_table": "materials", "managed": False,},
        ),
        migrations.CreateModel(
            name="Operation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "parameter_type1",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_value1",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_type2",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_value2",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_type3",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_value3",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_type4",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_value4",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_type5",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                (
                    "parameter_value5",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("required", models.IntegerField(blank=True, null=True)),
                ("planned_date", models.DateField(blank=True, null=True)),
                ("added_by", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "innaccordance_dec",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                ("complete", models.IntegerField(blank=True, null=True)),
                ("completion_date1", models.DateField(blank=True, null=True)),
                (
                    "confirmed_by1",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("completion_date2", models.DateField(blank=True, null=True)),
                (
                    "confirmed_by2",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("completion_date3", models.DateField(blank=True, null=True)),
                (
                    "confirmed_by3",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("completion_date4", models.DateField(blank=True, null=True)),
                (
                    "confirmed_by4",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("completion_date5", models.DateField(blank=True, null=True)),
                (
                    "confirmed_by5",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("notes", models.TextField(blank=True, null=True)),
                ("active", models.IntegerField(blank=True, null=True)),
                ("status", models.IntegerField(blank=True, null=True)),
                ("weight", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                (
                    "innaccordance_dec1",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "innaccordance_dec2",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "innaccordance_dec3",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "innaccordance_dec4",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
                (
                    "innaccordance_dec5",
                    models.CharField(blank=True, max_length=128, null=True),
                ),
            ],
            options={"db_table": "operations", "managed": False,},
        ),
        migrations.CreateModel(
            name="OperationDict",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("operationname", models.CharField(max_length=64)),
                ("parameter_type1", models.CharField(max_length=64)),
                ("parameter_type2", models.CharField(max_length=64)),
                ("parameter_type3", models.CharField(max_length=64)),
                ("parameter_type4", models.CharField(max_length=64)),
                ("parameter_type5", models.CharField(max_length=64)),
                ("defaultop", models.IntegerField()),
                ("defaultop_weight", models.IntegerField()),
                ("notes", models.TextField()),
                ("active", models.IntegerField()),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
            ],
            options={"db_table": "operation_dicts", "managed": False,},
        ),
        migrations.CreateModel(
            name="Pocastord",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_tech", models.IntegerField(blank=True, null=True)),
                ("cast_name", models.CharField(max_length=64)),
                ("cast_pcs", models.IntegerField()),
                ("material", models.CharField(blank=True, max_length=64, null=True)),
                ("cust_material", models.CharField(max_length=64)),
                ("pict_number", models.CharField(max_length=64)),
                ("model", models.IntegerField(blank=True, null=True)),
                ("rawcast", models.IntegerField(blank=True, null=True)),
                ("thermal", models.IntegerField(blank=True, null=True)),
                ("painting", models.IntegerField(blank=True, null=True)),
                ("mechrough", models.IntegerField(blank=True, null=True)),
                ("mechfine", models.IntegerField(blank=True, null=True)),
                ("castprice", models.FloatField(blank=True, null=True)),
                ("castworth", models.FloatField(blank=True, null=True)),
                ("other", models.TextField(blank=True, null=True)),
                ("aktywny", models.IntegerField(blank=True, null=True)),
                ("status", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
                ("total_weight", models.FloatField(blank=True, null=True)),
                ("planned_pcs", models.IntegerField(blank=True, null=True)),
            ],
            options={"db_table": "pocastords", "managed": False,},
        ),
        migrations.CreateModel(
            name="Porder",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("opis_zlecenia", models.CharField(max_length=128)),
                ("numer_oferty", models.CharField(max_length=32)),
                ("met_no", models.CharField(db_column="numer_MET", max_length=16)),
                ("data_zamowienia", models.DateField(blank=True, null=True)),
                ("nr_zamowienia", models.CharField(max_length=32)),
                (
                    "customer_date",
                    models.DateField(blank=True, db_column="termin_klienta", null=True),
                ),
                (
                    "confirmed_date",
                    models.DateField(
                        blank=True, db_column="termin_realizacji", null=True
                    ),
                ),
                (
                    "wprowadzajacy",
                    models.CharField(db_column="wprowadzajacy_id", max_length=20),
                ),
                ("data_przekwzt", models.DateField(blank=True, null=True)),
                ("data_wplywu_do_pzm", models.DateField(blank=True, null=True)),
                ("kontrolka_tech", models.DateField(blank=True, null=True)),
                ("kontrolka_plan", models.DateField(blank=True, null=True)),
                ("kontrolka_dkj", models.DateField(blank=True, null=True)),
                ("kontrolka_sp", models.DateField(blank=True, null=True)),
                ("data_wplywu_zlec_do_pzm", models.DateField(blank=True, null=True)),
                ("uwagi", models.TextField(blank=True, null=True)),
                ("aktywny", models.IntegerField(blank=True, null=True)),
                ("status", models.IntegerField(blank=True, null=True)),
                ("rodzaj", models.IntegerField(blank=True, null=True)),
                ("data_potw_zam", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
            ],
            options={"db_table": "porders", "managed": False,},
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("username", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("confirmation_code", models.CharField(max_length=255)),
                (
                    "remember_token",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("confirmed", models.IntegerField()),
                ("created_at", models.DateTimeField()),
                ("updated_at", models.DateTimeField()),
            ],
            options={"db_table": "users", "managed": False,},
        ),
    ]
