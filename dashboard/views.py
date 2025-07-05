from django.shortcuts import render,redirect
from movies.models import Movie 
from accounts.models import User
from bookings.models import Booking,BookingSeat
from django.contrib.auth.decorators import login_required
from payments.models import Payment

# Create your views here.

def home(request):
    movies = Movie.objects.all()
    context = {'movies': movies}
    return render(request,'dashboard/home.html',context)

def SearchView(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        movies = Movie.objects.filter(title__icontains=search_query)
        context = {'movies': movies}
        return render(request,'dashboard/home.html',context)
    return redirect('home')


@login_required
def YourOrders_View(request):
    user = request.user
    bookings = Booking.objects.filter(user=user,status='booked').order_by('-booking_time')
    tickets ={ Payment.objects.get(booking=booking):(BookingSeat.objects.filter(booking=booking),
                                                      check_cancellation(booking.showtime))
              for booking in bookings }
    context = {
                'tickets' : tickets,
               'user':user }
    return render(request, 'dashboard/orders.html', context)

from django.utils.timezone import now
from datetime import timedelta
def check_cancellation(showtime):
    now_time = now()
    buffer_time = now_time + timedelta(minutes=20)
    return showtime.showtime > buffer_time 

def sample_view(request):
    return render(request, 'dashboard/sample.html')