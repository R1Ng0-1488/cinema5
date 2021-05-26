from django.db import models
from django.utils import timezone

from order.models import Order
# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Movie model"""
    title = models.CharField(max_length=100)
    city = models.ManyToManyField(City)
    age_limit = models.ForeignKey('AgeLimit', on_delete=models.CASCADE)
    country = models.CharField(max_length=200)
    genres = models.CharField(max_length=200, blank=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    actors = models.CharField(max_length=200, blank=True)
    duration = models.TimeField(blank=True, null=True)
    poster = models.ImageField(upload_to='images/movies/%Y/%M/%D', blank=True)
    memorandum = models.DateField(auto_now_add=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(auto_now=True)
    premier = models.BooleanField(default=False)
    carousel = models.ImageField(upload_to='images/movies/carusel/%Y/%M/%D', blank=True)
    is_carousel = models.BooleanField(default=False)
    trailer = models.URLField(blank=True, null=True)
    # cinemas = models.ManyToManyField('Cinema')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('title',)


class AgeLimit(models.Model):
    """Age Limit model"""
    name = models.CharField(max_length=3)
    for_adults = models.BooleanField(default=True if name=='18+' else False)

    def __str__(self):
        return self.name


class Cinema(models.Model):
    """Cinema model"""
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    phone = models.CharField(max_length=11, default='')
    information = models.TextField(default='')
    halls = models.IntegerField(default=0)
    places = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} - {self.city}"


class Session(models.Model):
    """Session model"""
    date = models.DateField()
    time = models.TimeField()
    format = models.CharField(max_length=10)
    hall = models.ForeignKey('Hall', on_delete=models.CASCADE)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    # city = models.ForeignKey(City, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    price = models.IntegerField(default=228)

    def __str__(self):
        return f"{self.movie.title} - {self.date} - {self.time} - {self.cinema}"


class Hall(models.Model):
    """cinema hall"""
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Row(models.Model):
    row = models.IntegerField()
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)

    def __str__(self):
        return f"ряд {self.row} - {self.hall.name}"


class Place(models.Model):
    """place in the cinema hall"""
    row = models.ForeignKey(Row, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    empty = models.BooleanField(default=False)
    place = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Ряд №{self.row.row}, Место №{self.place}, {self.row.hall.name}"


class Ticket(models.Model):
    """ticket of place"""
    taken = models.BooleanField(default=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.place} - {self.session}"

    class Meta:
        unique_together = ('place', 'session')


class CinemaImages(models.Model):
    name = models.CharField(max_length=50)
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'cinema/{cinema.name}')

    def __str__(self):
        return self.name


class SocialLinks(models.Model):
    name = models.CharField(max_length=50)
    link = models.URLField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f'social_images/{city.name}', null=True, blank=True)

    def __str__(self):
        return self.name


class TitleQuestion(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Answer(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    tq = models.ForeignKey(TitleQuestion, on_delete=models.CASCADE)

    def __str__(self):
        return self.question