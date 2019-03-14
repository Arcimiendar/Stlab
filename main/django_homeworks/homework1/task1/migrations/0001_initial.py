# Generated by Django 2.1.7 on 2019-03-14 15:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sphere', models.CharField(max_length=200)),
                ('staff_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=200)),
                ('staff_amount', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='task1.Shop'),
        ),
    ]
