from django.contrib import admin
from .models import Booking,BookingSeat
# Register your models here.


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'showtime', 'total_amount', 'status','booking_time')

@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = ('booking', 'seat','showtime')