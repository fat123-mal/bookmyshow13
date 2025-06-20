# movies/admin.py

from django.contrib import admin
from .models import Movie, Theater, Seat, Booking, Showtime

class MovieAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'genre', 'language', 'rating']
    list_filter = ['genre', 'language']
    search_fields = ['name', 'cast'] # REMOVE: rating, cast, description

class TheaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # REMOVE: time

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'movie', 'theater')  # REMOVE: booked_at

admin.site.register(Movie, MovieAdmin)
admin.site.register(Theater, TheaterAdmin)
admin.site.register(Seat)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Showtime)
