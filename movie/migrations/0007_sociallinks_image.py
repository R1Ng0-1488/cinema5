# Generated by Django 3.1.3 on 2021-02-01 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0006_auto_20210201_1809'),
    ]

    operations = [
        migrations.AddField(
            model_name='sociallinks',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='social_images/None'),
        ),
    ]
