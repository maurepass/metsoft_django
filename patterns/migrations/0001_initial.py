# Generated by Django 2.2.4 on 2019-09-22 03:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pattern',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nazwa firmy')),
                ('drawing_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numer rysunku')),
                ('pattern_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nazwa odlewu')),
                ('last_order', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Ostatnie zlecenie')),
                ('orders_amount', models.IntegerField(blank=True, default=1, null=True, verbose_name='Ilość zleceń')),
                ('area', models.FloatField(blank=True, null=True, verbose_name='Powierzchnia')),
                ('layer_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numer ułożenia')),
                ('layer_place', models.CharField(blank=True, max_length=100, null=True, verbose_name='Miejsce ułożenia')),
                ('material', models.CharField(blank=True, max_length=30, null=True, verbose_name='Materiał')),
                ('cart_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Numer kartoteki')),
                ('pattern_index', models.CharField(blank=True, max_length=100, null=True, verbose_name='Numer indexu modelu')),
                ('verification', models.TextField(blank=True, null=True, verbose_name='Weryfikacja')),
                ('remarks', models.TextField(blank=True, null=True, verbose_name='Uwagi')),
                ('verification_date', models.CharField(blank=True, default=datetime.date.today, max_length=30, null=True, verbose_name='Data weryfikacji')),
                ('surname', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nazwisko')),
                ('move_in', models.DateField(blank=True, default=datetime.date.today, null=True, verbose_name='Data zmiany statusu')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'patterns',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PatternStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'PatternStatuses',
                'db_table': 'pattern_statuses',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PatternHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('pattern', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='patterns.Pattern')),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='patterns.PatternStatus')),
            ],
            options={
                'verbose_name_plural': 'PatternHistory',
                'db_table': 'pattern_history',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='pattern',
            name='status',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patterns.PatternStatus', verbose_name='status'),
        ),
    ]
