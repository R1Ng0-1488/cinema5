# Generated by Django 3.1.7 on 2021-04-13 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_advuser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='phone',
            field=models.CharField(default='89898957854', max_length=11, unique=True),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='username',
            field=models.CharField(blank=True, default='', max_length=35, null=True),
        ),
    ]
