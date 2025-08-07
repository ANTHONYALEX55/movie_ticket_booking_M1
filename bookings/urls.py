from django.urls import path 
from . import views 

urlpatterns = [
    path('showtimes/<slug>/<date_str>/',views.Theater_Showtime_View,name='theater_showtime'),
    path('seatselection/<int:show_id>/',views.Seat_Selection_View,name='seatselection'),
    path('book-ticket/<int:show_id>/',views.Book_Ticket_View,name='book_ticket'),
    path('canel-booking/<int:booking_id>/',views.cancel_booking,name='cancel_booking')

]