# Generated by Django 2.1.7 on 2019-03-17 10:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0007_auto_20190314_1539'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='comments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, null=True), size=None),
        ),
    ]