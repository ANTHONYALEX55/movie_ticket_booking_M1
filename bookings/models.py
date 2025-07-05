from django.db import models
from accounts.models import User 
from theaters.models import Showtime,Seat
# Create your models here.

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, default='pending',
                              
                    choices=[['pending','pending'],['cancelled','cancelled'],
                             ['booked','booked'],
                             ])
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)

class BookingSeat(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    showtime = models.ForeignKey(Showtime,on_delete=models.SET_NULL,null=True,blank=True)
