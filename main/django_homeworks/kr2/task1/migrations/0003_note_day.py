# Generated by Django 2.1.7 on 2019-03-22 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0002_auto_20190322_0822'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='day',
            field=models.DateField(blank=True, null=True),
        ),
    ]