# Generated by Django 2.2.10 on 2020-05-17 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="OrderStatus",
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
                ("status", models.CharField(max_length=50)),
                ("created_at", models.DateTimeField()),
            ],
            options={"db_table": "order_statuses",},
        ),
        migrations.CreateModel(
            name="Order",
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
                ("id_poc", models.IntegerField(blank=True, null=True)),
                (
                    "numer_met",
                    models.CharField(
                        blank=True,
                        db_column="numer_MET",
                        max_length=20,
                        null=True,
                        verbose_name="Numer zlecenia",
                    ),
                ),
                (
                    "company",
                    models.CharField(
                        blank=True, max_length=200, null=True, verbose_name="Klient"
                    ),
                ),
                (
                    "cast_name",
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name="Nazwa odlewu",
                    ),
                ),
                (
                    "cast_pcs",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="Ilość sztuk"
                    ),
                ),
                (
                    "pict_number",
                    models.CharField(
                        blank=True,
                        max_length=255,
                        null=True,
                        verbose_name="Numer rysunku",
                    ),
                ),
                (
                    "cust_material",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="Materiał"
                    ),
                ),
                (
                    "termin_klienta",
                    models.DateField(
                        blank=True, null=True, verbose_name="Termin klienta"
                    ),
                ),
                (
                    "model",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="Model"
                    ),
                ),
                (
                    "rawcast",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="Odlew"
                    ),
                ),
                (
                    "painting",
                    models.CharField(
                        blank=True, max_length=10, null=True, verbose_name="Malowanie"
                    ),
                ),
                (
                    "mechrough",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Obr. zgrubna",
                    ),
                ),
                (
                    "mechfine",
                    models.CharField(
                        blank=True,
                        max_length=10,
                        null=True,
                        verbose_name="Obr. na gotowo",
                    ),
                ),
                (
                    "marketing",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="Marketing"
                    ),
                ),
                (
                    "ord_in",
                    models.DateField(
                        blank=True, null=True, verbose_name="Data otrzymania"
                    ),
                ),
                (
                    "ord_out",
                    models.DateField(
                        blank=True, null=True, verbose_name="Data zakończenia"
                    ),
                ),
                ("working_time", models.IntegerField(blank=True, null=True)),
                ("important", models.IntegerField(blank=True, null=True)),
                (
                    "uwagi",
                    models.CharField(
                        blank=True, max_length=100, null=True, verbose_name="Uwagi"
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.ForeignKey(
                        blank=True,
                        default=2,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="tech_dep.OrderStatus",
                        verbose_name="Status",
                    ),
                ),
                (
                    "tech_memb",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"groups__name": "technologia"},
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Technolog",
                    ),
                ),
            ],
            options={"db_table": "orders",},
        ),
    ]
