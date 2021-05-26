from django.test import TestCase
from django.utils import timezone

from .models import (Movie, AgeLimit, Cinema,
                     Session, Hall, Place, Ticket)


class MovieModelTest(TestCase):
    """test Movie model"""

    def test_saving_and_retrieving_movie(self):
        """test database"""
        age_limit_1 = AgeLimit.objects.create(name='18+')
        age_limit_2 = AgeLimit.objects.create(name='12+')
        hall1 = Hall.objects.create(name='Hall 1')
        hall2 = Hall.objects.create(name='Hall 2')
        ticket = Ticket.objects.create(price=100, taken=False)
        places = [Place.objects.create(row=i, place=j, ticket=ticket) for i in range(10) for j in range(10)]
        for i in places:
            hall1.places.add(i)
            hall2.places.add(i)

        session1 = Session.objects.create(datetime=timezone.now(), hall=hall1)
        session2 = Session.objects.create(datetime=timezone.now(), hall=hall2)
        cinema1 = Cinema.objects.create(name='Guliver')
        cinema1.sessions.add(session1)
        cinema1.sessions.add(session2)
        cinema2 = Cinema.objects.create(name='North')
        cinema2.sessions.add(session1)
        cinema2.sessions.add(session2)
        today = timezone.now()
        movie1 = Movie.objects.create(title='Ololo', age_limit=age_limit_1,
                                      country='USA', start_date=today+timezone.timedelta(days=10),
                                      end_date=today+timezone.timedelta(days=20))
        movie2 = Movie.objects.create(title='Ololo2', age_limit=age_limit_2,
                                      country='Russia', start_date=today, end_date=today+timezone.timedelta(days=10))
        movie1.cinemas.add(cinema1)
        movie1.cinemas.add(cinema2)
        movie2.cinemas.add(cinema1)
        movie2.cinemas.add(cinema2)

        self.assertEqual(movie1.end_date, today+timezone.timedelta(days=20))
        self.assertEqual(movie2.end_date, today+timezone.timedelta(days=10))
        self.assertEqual([i for i in movie1.cinemas.all()], [cinema1, cinema2])
        self.assertEqual([i for i in cinema1.sessions.all()], [session1, session2])
        self.assertEqual(session1.hall, hall1)
        self.assertEqual(session2.hall, hall2)
        self.assertEqual(len(hall1.places.all()), 100)
        self.assertEqual(len(hall2.places.all()), 100)
        self.assertEqual(ticket.price, 100)
        self.assertEqual(ticket.taken, False)
        self.assertEqual(movie1.country, 'USA')
        self.assertEqual(movie2.country, 'Russia')
        self.assertEqual(movie1.age_limit.name, '18+')
        self.assertEqual(movie2.age_limit.name, '12+')
