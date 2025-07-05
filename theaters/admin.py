from django.contrib import admin
from .models import Theater,Seat,Showtime
# Register your models here.

@admin.register(Theater)
class Theatermodeladmin(admin.ModelAdmin):
    list_display = ['name','city','address']

@admin.register(Seat)
class SeatmodelAdmin(admin.ModelAdmin):
    list_display = [ 'theater','row_label','seat_number','seat_type']

@admin.register(Showtime)
class ShowtimeAdmin(admin.ModelAdmin):
    list_display = ['showtime','theater','movie','gold_price','silver_price','recliner_price']