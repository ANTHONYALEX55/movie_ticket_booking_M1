from django.shortcuts import render,redirect
from theaters.models import Theater,Showtime
from movies.models import Movie 
from django.db.models import Q
from django.http import HttpResponse
from datetime import datetime, timedelta,date
from theaters.models import Seat,Showtime
from django.contrib.auth.decorators import login_required 
from .models import Booking,BookingSeat
import json
from accounts.models import User
from django.conf import settings
from django.contrib import messages



# Create your views here.

def Theater_Showtime_View(request,slug,date_str):
    today = datetime.today().date()
    start_date = today - timedelta(days=0) 
    week = []
    for i in range(7):
        day = start_date + timedelta(days=i)
        week.append({
            'name': day.strftime("%a").upper(),
            'day': day.day,
            'month': day.strftime("%b").upper(),
            'date': day
        })
    if not Movie.objects.filter(slug=slug).exists():
        return HttpResponse('Invalid request')
    movie = Movie.objects.get(slug=slug)

    selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    if selected_date == datetime.now().date():
        theater_showtimes = [Showtime.objects.filter(movie=movie,showtime__date = selected_date,showtime__time__gt=datetime.now().time(),
                            theater=theater).order_by('showtime') for theater in Theater.objects.all()
                if Showtime.objects.filter(movie=movie,showtime__date = selected_date,showtime__time__gt=datetime.now().time()
                                           ,theater=theater).exists()  ]
    else:
        theater_showtimes = [Showtime.objects.filter(movie=movie,showtime__date = selected_date,
                            theater=theater).order_by('showtime') for theater in Theater.objects.all()
                if Showtime.objects.filter(movie=movie,showtime__date = selected_date
                                           ,theater=theater).exists()  ]

    context = {
        'movie': movie,
        'theater_showtimes': theater_showtimes,
        'week': week,
        'today': selected_date,
        'slug' : slug
    }
    return render(request,'theaters/showtimes.html',context)


def Seat_Selection_View(request,show_id):
    showtime = Showtime.objects.get(id = show_id)
    theater = showtime.theater
    movie = showtime.movie
    seats = Seat.objects.filter(theater=theater).order_by('-row_label','seat_number')
    seat_rows = {}
    booked_seats = [ booking_seat.seat  for booking_seat in BookingSeat.objects.filter(showtime=showtime)]
    for seat in seats:
        row = (seat.row_label,seat.seat_type)
        if row not in seat_rows:
            seat_rows[row] = []
        if seat not in booked_seats:
            seat_rows[row].append(seat)
        else: 
            seat_rows[row].append(0)
    context = {
        'movie':movie,
        'theater': theater,
        'seats':seats,
        'showtime':showtime,
        'seat_rows':seat_rows
    }
    return render(request,'theaters/seatselection.html',context)
    


@login_required
def Book_Ticket_View(request,show_id):
    if request.method=='POST':
        selected_seats = json.loads(request.POST['selected_seats'])
        total_amount = eval(request.POST['total_amount'])
        tickets = []
        user = User.objects.get(username = request.user.username)
        showtime = Showtime.objects.get(id=show_id)
        convenience_fee = total_amount * 0.1
        sub_total = total_amount + convenience_fee 
        booking = Booking.objects.create(user=user,
                                         showtime=showtime,
                                         total_amount=sub_total)        
        for seat in selected_seats:
            tickets.append(seat['key']) 
            id = seat['id']
            seat_obj = Seat.objects.get(id=id)
            BookingSeat.objects.create(
                booking=booking,
                seat = seat_obj,
                showtime=showtime
            )
        context = {
            'tickets':tickets,
            'convenience_fee' : convenience_fee,
            'sub_total':sub_total,
            'total_amount': total_amount,
            'showtime':showtime,
            'booking':booking,
            'stripe_public_key' : settings.STRIPE_PUBLIC_KEY
           

        }
        return render(request,'bookings/proceed_to_payment.html',context)
    return HttpResponse('Invalid Request')
            
@login_required
def cancel_booking(request,booking_id):
    booking = Booking.objects.get(id=booking_id)
    booking.booking_status = 'cancelled'
    booking.save()
    qs = BookingSeat.objects.filter(booking=booking)
    qs.delete()
    messages.error(request,'your booking have been cancelled amount refunded to your bank account')
    return redirect('yourorders')

