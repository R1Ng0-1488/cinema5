# Generated by Django 3.1.7 on 2021-04-17 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_advuser_bonuses'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='advuser',
            name='phone',
            field=models.CharField(default='', max_length=11, unique=True),
        ),
    ]
