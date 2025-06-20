from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Theater, Seat, Booking, Showtime
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse  # ✅ Needed for test_email view


def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})


def movie_list(request):
    all_genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Thriller']
    all_languages = ['English', 'Hindi', 'Kannada', 'Malayalam', 'Tamil', 'Telugu']

    selected_genres = request.GET.getlist('genre')
    selected_languages = request.GET.getlist('language')
    search_query = request.GET.get('search', '')

    movies = Movie.objects.all()

    if selected_genres:
        movies = movies.filter(genre__in=selected_genres)
    if selected_languages:
        movies = movies.filter(language__in=selected_languages)
    if search_query:
        movies = movies.filter(name__icontains=search_query)

    context = {
        'movies': movies,
        'genre_options': all_genres,
        'language_options': all_languages,
        'selected_genres': selected_genres,
        'selected_languages': selected_languages
    }
    return render(request, 'movies/movie_list.html', context)


def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theater = Theater.objects.filter(movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theater})


def showtimes(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    showtimes = Showtime.objects.filter(movie=movie).order_by('show_time')
    return render(request, 'movies/showtimes.html', {'movie': movie, 'showtimes': showtimes})


@login_required
def select_seats(request, showtime_id):
    showtime = get_object_or_404(Showtime, id=showtime_id)
    seats = Seat.objects.filter(theater=showtime.theater).order_by('seat_number')
    now = timezone.now()

    if request.method == 'POST':
        selected_seat_ids = request.POST.getlist('seats')
        selected_seats = Seat.objects.filter(id__in=selected_seat_ids, is_booked=False)

        for seat in selected_seats:
            seat.is_booked = True
            seat.reserved_by = request.user
            seat.reserved_until = None
            seat.save()

        seat_numbers = [seat.seat_number for seat in selected_seats]
        subject = "Your Movie Ticket Booking Confirmation"
        message = f"""
Dear {request.user.username},

Thank you for booking with BookMySeat!

🎬 Movie: {showtime.movie.name}
🏢 Theater: {showtime.theater.name}
🗓️ Date: {showtime.show_date.strftime('%d %B %Y')}
🕒 Time: {showtime.show_time.strftime('%I:%M %p')}
🎺 Seats: {', '.join(seat_numbers)}

Enjoy your show!
"""

        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
                fail_silently=False
            )
        except Exception as e:
            print("Email send error:", e)

        return redirect('home')

    context = {
        'showtime': showtime,
        'seats': seats,
        'now': now
    }
    return render(request, 'movies/select_seats.html', context)


@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(theater=theater)
    now = timezone.now()

    showtime = Showtime.objects.filter(theater=theater).first()
    if not showtime:
        return render(request, "movies/book_seat.html", {
            'theater': theater,
            'seats': seats,
            'error': "No showtime available for this theater."
        })

    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []

        if not selected_seats:
            return render(request, "movies/book_seat.html", {
                'theater': theater,
                'seats': seats,
                'error': "No seat selected"
            })

        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, theater=theater)

            if seat.is_booked or (seat.reserved_until and seat.reserved_until > now and seat.reserved_by != request.user):
                error_seats.append(seat.seat_number)
                continue

            try:
                Booking.objects.create(
                    user=request.user,
                    seat=seat,
                    movie=theater.movie,
                    theater=theater,
                    showtime=showtime
                )
                seat.is_booked = True
                seat.reserved_by = None
                seat.reserved_until = None
                seat.save()

                try:
                    send_mail(
                        '🎫 Ticket Confirmation - BookMySeat',
                        f'Dear {request.user.username},\n\n'
                        f'Your ticket is confirmed!\n\n'
                        f'Movie: {theater.movie.name}\n'
                        f'Theater: {theater.name}\n'
                        f'Date: {showtime.show_date.strftime("%d %B %Y")}\n'
                        f'Time: {showtime.show_time.strftime("%I:%M %p")}\n'
                        f'Seat: {seat.seat_number}\n\n'
                        f'Enjoy your show!',
                        settings.DEFAULT_FROM_EMAIL,
                        [request.user.email],
                        fail_silently=False
                    )
                except Exception as e:
                    print("Email send error:", e)

            except IntegrityError:
                error_seats.append(seat.seat_number)

        if error_seats:
            error_message = f"The following seats are already booked or reserved: {', '.join(error_seats)}"
            return render(request, 'movies/book_seat.html', {
                'theater': theater,
                'seats': seats,
                'error': error_message
            })

        return redirect('profile')

    return render(request, 'movies/book_seat.html', {
        'theater': theater,
        'seats': seats
    })


def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'movies/booking_confirmation.html', {'booking': booking})


# ✅ Test Email Sending (Debug View)
def test_email(request):
    from django.core.mail import send_mail
    from django.conf import settings
    from django.http import HttpResponse

    try:
        send_mail(
            subject='✅ Test Email from Django',
            message='This is a test email to check your SMTP settings.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['fathimaabdullatheef278@gmail'],  # use your email
            fail_silently=False
        )
        return HttpResponse("✅ Email sent successfully.")
    except Exception as e:
        return HttpResponse(f"❌ Email send error: {str(e)}")