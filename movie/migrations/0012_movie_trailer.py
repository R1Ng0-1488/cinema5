# Generated by Django 3.1.7 on 2021-04-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0011_auto_20210319_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='trailer',
            field=models.URLField(blank=True, null=True),
        ),
    ]
