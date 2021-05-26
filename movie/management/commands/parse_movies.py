from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup as BS
from selenium import webdriver
from datetime import date, time
from time import sleep
from django.conf import settings

import requests
import re
import os

from movie.models import Movie, Cinema, City, AgeLimit

from fake_useragent import UserAgent

useragent = UserAgent()

MOVIES = [m.title for m in Movie.objects.all()]


class ParserCinema5:

    def __init__(self, url):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Accept-Language': 'ru'
        }
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.set_preference('general.useragent.override', f'{useragent.random}')
        firefox_options.binary_location = r'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
        self.url = url
        self.browser = webdriver.Firefox(options=firefox_options)
        self.browser.get(url)

    def parse_all_movie(self):
        soup = self.get_page()
        j = 0
        for i in [i.get_attribute('data-cb-id') for i in self.browser.find_elements_by_xpath('//a[@data-cb-id]')]:
            new_url = self.url + 'movie/' + i
            self.parse_one_movie(new_url, j)
            j += 1

    def parse_one_movie(self, new_url, j):
        # распидарасить дикт валуе на переменный, преобразовать строку ДатаТайм в тип дататайм
        self.browser.get(new_url)
        self.browser.implicitly_wait(10)
        page = str(self.browser.page_source)
        s = BS(page, 'html.parser')
        title = s.find('div', class_='wcbox__movie-title').text
        age_limit = s.find('div', class_='wcbox__movie-age').text
        values = s.find_all('div', class_='wcbox__movie-meta__item')
        values = {value.find('div', class_='wcbox__movie-meta__name').text: value.find('div',
                                                                                       class_='wcbox__movie-meta__value').text
                  for value in values if value}
        description = s.find('div', class_='wcbox__movie-description').text
        poster = re.split('["]', s.find('div', class_='wcbox__movie-poster_cover').get('style'))[-2]
        country = values.get('Производство')
        genre = values.get('Жанры')
        director = values.get('Режисёр')
        actors = values.get('В главных ролях')
        memorandum = self.get_dates(values.get(' Меморандум '))
        duration = self.get_time(values.get('Длительность'))

        pos = requests.get(poster)
        path = os.path.join(settings.MEDIA_ROOT, 'images')

        with open(path + f'\\movies\\2020\\image{j}.jpg', 'wb') as f:
            f.write(pos.content)
        try:
            if title not in MOVIES:
                a = Movie.objects.create(title=title,
                                     age_limit=AgeLimit.objects.get_or_create(name=age_limit)[0], poster=path+f'\\movies\\2020\\image{j}.jpg',
                                     genres=genre, country=country, director=director, actors=actors, memorandum=memorandum,
                                     description=description, duration=duration)
                for city in City.objects.all():
                    a.city.add(city)
            # for cinema in Cinema.objects.all():
            #     a.cinemas.add(cinema)
                print(j)
        except:
            pass
        # print(title, age_limit, poster, genre, country, director, actors, memorandum, duration, description)

    def get_page(self):
        r = self.session.get(self.url)
        return BS(r.text, 'html.parser')

    def get_time(self, time_str):
        time_int = [int(i) for i in re.findall(r'\d+', time_str)]
        if len(time_int) == 1:
            if 'мин' in time_str:
                return time(0, *time_int)
            else:
                return time(*time_int)

        return time(*time_int)

    def get_dates(self, date_str):
        if date_str:
            date_list = [int(i) for i in re.split(r'[ .]', date_str)[1:]]
            return date(*date_list[::-1])

    def quit_browser(self):
        self.browser.quit()


class Command(BaseCommand):
    help = "Парсинг фильмов из сайта cinema5.ru"

    def handle(self, *args, **options):
        url = 'https://cinema5.ru/orenburg/tomorrow#/'
        ps = ParserCinema5(url)
        ps.parse_all_movie()
        ps.quit_browser()