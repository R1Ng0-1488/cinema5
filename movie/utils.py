from django.utils import timezone

from .models import Session, City


class SessionFilter:
    def get_sessions(self, city_slug):
        return Session.objects.filter(cinema__city=City.objects.get(slug=city_slug))


class SessionFilterToday(SessionFilter):
    def get_sessions(self, city_slug):
        now = timezone.now().time()
        return super().get_sessions(city_slug) \
            .filter(date=timezone.localdate()) \
            .filter(time__gte=now) \
            .filter(active=True)


class SessionFilterTomorrow(SessionFilter):
    def get_sessions(self, city_slug):
        return super().get_sessions(city_slug)\
            .filter(date=timezone.localdate() + timezone.timedelta(days=1))\
            .filter(active=True)


class SessionFilterSoon(SessionFilter):
    def get_sessions(self, city_slug):
        return super().get_sessions(city_slug)\
            .filter(date__gte=timezone.localdate() + timezone.timedelta(days=30))


class SessionFilterDate(SessionFilter):
    def get_sessions(self, date, city_slug):
        sessions = super().get_sessions(city_slug).filter(active=True).filter(date=date)
        if date == timezone.localdate():
            return sessions\
                .filter(time__gte=timezone.now().time())
        return sessions
