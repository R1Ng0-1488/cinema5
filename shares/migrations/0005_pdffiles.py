# Generated by Django 3.1.3 on 2021-01-28 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0004_share_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='PdfFiles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('desc', models.TextField()),
                ('file', models.FileField(upload_to='pdf_files')),
            ],
        ),
    ]