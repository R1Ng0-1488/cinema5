from django import template
from django.utils import timezone

from ..utils import *
from ..models import City, Ticket, Session, Place

register = template.Library()


@register.filter(name='is_ticket')
def is_ticket(obj, session):
    place = Place.objects.get(id=obj)
    session = Session.objects.get(id=session)
    try:
        Ticket.objects.get(session=session, place=place)
        return True
    except Ticket.DoesNotExist:
        return False


@register.filter(name='session_count_today')
def session_count_today(obj, city_slug):
    s = SessionFilterToday()
    return s.get_sessions(city_slug).filter(movie=obj).count()


@register.filter(name='session_movie_today')
def session_movie_today(obj, city_slug):
    s = SessionFilterToday()
    return s.get_sessions(city_slug).filter(movie=obj)


@register.filter(name='session_count_tomorrow')
def session_count_tomorrow(obj, city_slug):
    s = SessionFilterTomorrow()
    return s.get_sessions(city_slug).filter(movie=obj).count()


@register.filter(name='session_movie_tomorrow')
def session_movie_tomorrow(obj, city_slug):
    s = SessionFilterTomorrow()
    return s.get_sessions(city_slug).filter(movie=obj)


@register.filter(name='session_count_soon')
def session_count_soon(obj, city_slug):
    s = SessionFilterSoon()
    return s.get_sessions(city_slug).filter(movie=obj).count()


@register.filter(name='session_movie_soon')
def session_movie_soon(obj, city_slug):
    s = SessionFilterSoon()
    return s.get_sessions(city_slug).filter(movie=obj)


@register.filter(name='session_count_date')
def session_count_date(obj, date):
    date, city_slug = date
    s = SessionFilterDate()
    return s.get_sessions(date, city_slug).filter(movie=obj).count()


@register.filter(name='session_movie_date')
def session_movie_date(obj, date):
    date, city_slug = date
    s = SessionFilterDate()
    return s.get_sessions(date, city_slug).filter(movie=obj)