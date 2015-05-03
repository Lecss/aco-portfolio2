# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('profit_year', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('budget', models.FloatField(default=0)),
                ('duration', models.IntegerField(default=10)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('fail', models.FloatField(default=0.0)),
                ('cost', models.FloatField(default=0)),
                ('duration', models.IntegerField(default=0)),
                ('drug', models.ForeignKey(to='portfolio.Drug')),
            ],
        ),
        migrations.AddField(
            model_name='drug',
            name='portfolio',
            field=models.ForeignKey(to='portfolio.Portfolio'),
        ),
    ]
