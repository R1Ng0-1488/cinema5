# Generated by Django 3.1.3 on 2021-02-07 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_auto_20210207_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='qr_code',
            field=models.ImageField(blank=True, upload_to='qr_codes/%Y/%M/%M'),
        ),
    ]
