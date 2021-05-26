from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import time, timedelta

from movie.models import *


def create_sessions():
    d1 = timezone.localdate()
    d2 = timezone.localdate() + timedelta(days=1)
    d3 = timezone.localdate() + timedelta(days=40)
    t = time(20, 40)
    f = '2D'
    h = Hall.objects.first()
    cs = Cinema.objects.all()

    for m in Movie.objects.all()[:5]:
        Session.objects.create(date=d1, time=t, format=f, hall=h, cinema=cs[0], movie=m)

    for m in Movie.objects.all():
        Session.objects.create(date=d1, time=t, format=f, hall=h, cinema=cs[1], movie=m)

    for m in Movie.objects.all()[:5]:
        Session.objects.create(date=d2, time=t, format=f, hall=h, cinema=cs[2], movie=m)

    for m in Movie.objects.all():
        Session.objects.create(date=d3, time=t, format=f, hall=h, cinema=cs[4], movie=m)


class Command(BaseCommand):
    help = "Create sessions"

    def handle(self, *args, **options):
        create_sessions()