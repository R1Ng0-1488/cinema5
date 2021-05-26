from movie.models import City, Movie
from django.core.cache import cache
from django.conf import settings
import redis

r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)


def cities(request):
    context = dict()
    context['cities'] = City.objects.all()
    if r.get('const_city'):
        context['city_slug'] = r.get('const_city').decode()
        print('------>>>>>', context['city_slug'])
    # context['city_slug'] = cache.get('city')
    context['date_now'] = request.GET.get('date', None)
    try:
        context['city_name'] = City.objects.get(slug=context['city_slug'])
        context['carousel_first_movie'] = Movie.objects.filter(is_carousel=True)[0]
        context['carousel_movies'] = Movie.objects.filter(is_carousel=True)[1:]
    except:
        pass
    # context['city'] = City.objects.get(slug=context['city_slug'])
    try:
        context['cinema_pk'] = City.objects.get(slug=context['city_slug']).cinema_set.first().pk
    except:
        pass
    return context
