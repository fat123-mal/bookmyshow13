from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/theaters/', views.theater_list, name='theater_list'),
    path('showtimes/<int:movie_id>/', views.showtimes, name='showtimes'),
    path('select-seats/<int:showtime_id>/', views.select_seats, name='select_seats'),
    path('book-seats/<int:theater_id>/', views.book_seats, name='book_seats'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('test-email/', views.test_email, name='test_email'),
]
