# Generated by Django 3.1.3 on 2021-03-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0007_auto_20210128_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]