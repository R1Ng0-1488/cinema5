# Generated by Django 3.1.3 on 2020-12-30 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0002_auto_20201221_1818'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('place', 'session')},
        ),
    ]
