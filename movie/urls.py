from django.urls import path
from . import views


urlpatterns = [
    path('', views.CitiesView.as_view(), name='cities'),
    path('<slug:slug>/today', views.MovieTodayView.as_view(), name='today'),
    path('<slug:slug>/children', views.MovieChildrenTodayView.as_view(), name='children'),
    path('<slug:slug>/date', views.MovieDateView.as_view(), name='filter'),
    path('<slug:slug>/tomorrow', views.MovieTomorrowView.as_view(), name='tomorrow'),
    path('<slug:slug>/soon', views.MovieSoonView.as_view(), name='soon'),
    path('<slug:slug>/today/<int:pk>', views.MovieDetailToday.as_view(), name='movie_detail_today'),
    path('<slug:slug>/tomorrow/<int:pk>', views.MovieDetailTomorrow.as_view(), name='movie_detail_tomorrow'),
    path('<slug:slug>/soon/<int:pk>', views.MovieDetailSoon.as_view(), name='movie_detail_soon'),
    path('<slug:slug>/date/<str:date>/<int:pk>', views.MovieDetailDate.as_view(), name='movie_detail_date'),
    path('<slug:slug>/shows/<int:pk>', views.SessionDetail.as_view(), name='session_detail'),
    path('<slug:slug>/shows/<int:pk>/create/ticket', views.CreateTicket.as_view(), name='create_ticket'),
    path('<slug:slug>/support/', views.SupportView.as_view(), name='support'),
    path('<slug:slug>/about/<int:pk>', views.AboutView.as_view(), name='about'),
    path('<slug:slug>/questions', views.TitleQuestionView.as_view(), name='questions'),
    path('<slug:slug>/questions/<int:pk>', views.AnswerDetailView.as_view(), name='answer'),
]

