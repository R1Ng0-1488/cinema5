from django.db import models

from movie.models import City
# Create your models here.


class Share(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    image = models.ImageField(upload_to='shares')
    slug = models.SlugField(max_length=20)
    city = models.ManyToManyField(City)

    def __str__(self):
        return self.title


class PdfFiles(models.Model):
    title = models.CharField(max_length=20)
    desc = models.TextField()
    file = models.FileField(upload_to='pdf_files')
    slug = models.SlugField(max_length=20)

    def __str__(self):
        return self.title
