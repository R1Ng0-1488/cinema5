# Generated by Django 3.1.3 on 2021-02-07 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_auto_20210207_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
