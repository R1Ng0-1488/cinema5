# Generated by Django 3.1.7 on 2021-04-13 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_remove_advuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='username',
            field=models.CharField(default='', max_length=35),
        ),
    ]
