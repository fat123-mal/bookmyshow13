from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Genre and Language Choices
GENRE_CHOICES = [
    ('Action', 'Action'),
    ('Comedy', 'Comedy'),
    ('Drama', 'Drama'),
    ('Horror', 'Horror'),
    ('Romance', 'Romance'),
    ('Thriller', 'Thriller'),
]

LANGUAGE_CHOICES = [
    ('English', 'English'),
    ('Hindi', 'Hindi'),
    ('Malayalam', 'Malayalam'),
    ('Tamil', 'Tamil'),
    ('Telugu', 'Telugu'),
    ('Kannada', 'Kannada'),
]

class Movie(models.Model):
    name = models.CharField(max_length=255)
    rating = models.CharField(max_length=10, default='Not Rated')  # Movie rating
    cast = models.TextField(blank=True, null=True)  # Movie cast
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, default='Action')
    language = models.CharField(max_length=50, choices=LANGUAGE_CHOICES, default='English')
    description = models.TextField(blank=True, null=True)          # Description
    image = models.CharField(max_length=100)  # Path to image filename

    def __str__(self):
        return self.name

class Theater(models.Model):
    name = models.CharField(max_length=255)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie.name}"

class Seat(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    # 🟡 For Task 7: Seat Reservation Timeout
    reserved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    reserved_until = models.DateTimeField(null=True, blank=True)

    def is_reserved(self):
        return self.reserved_until and self.reserved_until > timezone.now()

    def __str__(self):
        return f"Seat {self.seat_number} in {self.theater.name}"

class Showtime(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    show_date = models.DateField()
    show_time = models.TimeField()

    def __str__(self):
        return f"{self.movie.name} at {self.theater.name} on {self.show_date} {self.show_time}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE, null=True, blank=True)
    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.seat.seat_number} ({self.movie.name})"
