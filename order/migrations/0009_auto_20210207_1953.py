# Generated by Django 3.1.3 on 2021-02-07 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_auto_20210207_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='url',
            field=models.CharField(blank=True, default='127.0.0.1:8000/<built-in function id>', max_length=200),
        ),
    ]
