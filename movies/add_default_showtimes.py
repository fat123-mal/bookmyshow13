from datetime import datetime, timedelta, time
from django.utils import timezone
from movies.models import Movie, Theater, Showtime

def add_default_showtimes():
    today = timezone.localdate()
    tomorrow = today + timedelta(days=1)
    show_times = [time(14, 0), time(18, 30), time(21, 0)]  # 2:00 PM, 6:30 PM, 9:00 PM

    for movie in Movie.objects.all():
        theaters = Theater.objects.filter(movie=movie)
        for theater in theaters:
            for show_date in [today, tomorrow]:
                for show_time in show_times:
                    if not Showtime.objects.filter(movie=movie, theater=theater, show_date=show_date, show_time=show_time).exists():
                        Showtime.objects.create(
                            movie=movie,
                            theater=theater,
                            show_date=show_date,
                            show_time=show_time
                        )
    print("✅ Default showtimes added successfully.")
