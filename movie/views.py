from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from datetime import date, timedelta, datetime
from django.utils import timezone
from django.views.generic import View, ListView, DetailView, CreateView
from django.http import JsonResponse
from django.db import IntegrityError
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q

import re
import redis

from .session import SessionTickets
from .models import *
from .utils import *
from .forms import TicketForm
from .tasks import delete_tickets_if_invalid


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)


class CityMixin(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['city'] = City.objects.get(slug=str(self.request.path.split('/')[1]))
        d = self.request.GET.get('date', None)
        context['city_slug'] = str(self.request.path.split('/')[1])
        if d:
            context['date_form'] = d
            c = context['city_slug']
            m = kwargs['object']
            d = date(*[int(i) for i in d.split('-')])
            sessions = SessionFilterDate().get_sessions(d, c)
            sessions = sessions.filter(movie=m)
            sessions = [sessions.filter(cinema=cinema) for cinema in context['city'].cinema_set.all()]
            context['sessions2'] = sessions
            context['sessions_flag'] = True
            # print([i for i in context['sessions']])
        # print([cinema for cinema in context['city'].cinema_set.all()])
        # print(context)
        return context


class CitiesView(View):
    queryset = City.objects.all()
    template_name = 'movie/city_list.html'

    def get(self, request):
        if r.get('temp_city'):
            return redirect('today', slug=r.get('temp_city').decode())
        if r.get('const_city'):
            r.delete('const_city')
        # if cache.has_key('city'):
        #     city = cache.get('city')
        #     return redirect('today', slug=city)
        return render(request, self.template_name, {'object_list': self.queryset})


class MovieTodayView(SessionFilterToday, ListView):

    def get_queryset(self):
        city_slug = self.request.path.split('/')[1]
        
        if not r.get('temp_city'):
            r.setex('temp_city', timedelta(minutes=60), city_slug)
        r.set('const_city', city_slug)
        # self.request.session['city'] = city_slug
        # if not cache.has_key('city'):
        #     cache.set('city', city_slug, 60 * 15)
        queryset = Movie.objects.filter(session__in=self.get_sessions(city_slug))
        return queryset.distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['today'] = True
        return context


class MovieChildrenTodayView(SessionFilterToday, ListView):
    # template_name = 'movie/children_list.html'

    def get_queryset(self):
        city_slug = self.request.path.split('/')[1]
        queryset = Movie.objects.filter(session__in=self.get_sessions(city_slug))
        return queryset.filter(Q(age_limit__name='0+') | Q(age_limit__name='6+')).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['children'] = True
        return context


class MovieTomorrowView(SessionFilterTomorrow, ListView):
    def get_queryset(self):
        city_slug = self.request.path.split('/')[1]
        return Movie.objects.filter(session__in=self.get_sessions(city_slug)).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tomorrow'] = True
        return context


class MovieSoonView(SessionFilterSoon, ListView):
    def get_queryset(self):
        city_slug = self.request.path.split('/')[1]
        return Movie.objects.filter(session__in=self.get_sessions(city_slug)).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['soon'] = True
        return context


class MovieDateView(SessionFilterDate, ListView):
    def get_queryset(self):
        city_slug = self.request.path.split('/')[1]
        d = date(*[int(i) for i in self.request.GET.get('date').split('-')])
        sessions = self.get_sessions(d, city_slug)
        return Movie.objects.filter(session__in=sessions).distinct()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['city_slug'] = str(self.request.path.split('/')[1])
        context['date'] = (date(*[int(i) for i in self.request.GET.get('date').split('-')]), context['city_slug'])
        context['date0'] = context['date'][0]
        return context


class MovieDetailToday(CityMixin, SessionFilterToday):
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['today'] = True
        sessions = self.get_sessions(city_slug=context['city_slug']).filter(movie=kwargs['object'])
        sessions = [sessions.filter(cinema=cinema) for cinema in context['city'].cinema_set.all()]
        context['sessions'] = sessions
        return context


class MovieDetailTomorrow(CityMixin, SessionFilterTomorrow):
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tomorrow'] = True
        sessions = self.get_sessions(city_slug=context['city_slug']).filter(movie=kwargs['object'])
        context['sessions'] = [sessions.filter(cinema=cinema) for cinema in context['city'].cinema_set.all()]
        return context


class MovieDetailSoon(CityMixin, SessionFilterSoon):
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['soon'] = True
        sessions = self.get_sessions(city_slug=context['city_slug']).filter(movie=kwargs['object'])
        context['sessions'] = [sessions.filter(cinema=cinema) for cinema in context['city'].cinema_set.all()]
        return context


class MovieDetailDate(CityMixin, SessionFilterDate):
    model = Movie

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['city_slug'] = str(self.request.path.split('/')[1])
        context['date'] = (date(*[int(i) for i in self.request.path.split('/')[3].split('-')]), context['city_slug'])
        sessions = self.get_sessions(city_slug=context['city_slug'], date=context['date'][0]).filter(movie=kwargs['object'])
        context['sessions'] = [sessions.filter(cinema=cinema) for cinema in context['city'].cinema_set.all()]
        return context


class SessionDetail(DetailView):
    model = Session

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['errors'] = messages.get_messages(self.request)
        return context


class CreateTicket(View):
    def post(self, request, slug, pk):
        session = SessionTickets(request)
        form = TicketForm(request.POST)
        if form.is_valid():
            try:
                tickets = form.save()
                now = timezone.now()
                delete_tickets_if_invalid.apply_async([tickets], eta=now + timedelta(minutes=1))
            except IntegrityError:
                messages.add_message(request, messages.ERROR, "Билет(ы) уже куплены")
                return redirect('session_detail', slug=slug, pk=pk)
            session.add(tickets)
            return redirect('order_create', slug=slug)
        else:
            messages.add_message(request, messages.ERROR, "Билет(ы) уже куплены")
            return redirect('session_detail', slug=slug, pk=pk)


class SupportView(View):
    def get(self, request, slug):
        return render(request, 'about/support.html')


class AboutView(CityMixin):
    model = Cinema

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cinemas'] = Cinema.objects.filter(city__slug=context['city_slug'])
        context['first'] = kwargs['object'].cinemaimages_set.first()
        context['rest'] = kwargs['object'].cinemaimages_set.all()[1:]
        return context


class TitleQuestionView(ListView):
    model = TitleQuestion


class AnswerDetailView(DetailView):
    model = Answer

    def get(self, request, *args, **kwargs):
        detail = self.get_object()
        return JsonResponse({'answer': detail.answer}, safe=False)


