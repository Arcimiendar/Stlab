# Generated by Django 2.1.7 on 2019-03-22 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='position',
            field=models.CharField(choices=[('Professor', 'Professor'), ('Assistant professor', 'Assistant professor'), ('Graduate student', 'Graduate student'), ('Assistant', 'Assistant')], max_length=128),
        ),
    ]
