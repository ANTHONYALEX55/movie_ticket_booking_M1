from django.db import models
from movies.models import Movie
# Create your models here.

class Theater(models.Model):
    name = models.CharField(max_length=2000)
    city = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name
    
    def add_seat(self,row_label,seat_type,seat_range):
        for i in seat_range:
            Seat.objects.create(theater=self,row_label=row_label,seat_type=seat_type,seat_number=i)


seat_type_choices = [
    ['silver','silver'],['gold','gold'],['RECLINER','RECLINER']
]
class Seat(models.Model):
    theater = models.ForeignKey(Theater,on_delete=models.CASCADE)
    seat_number = models.IntegerField()
    row_label = models.CharField(max_length=1)
    seat_type = models.CharField(max_length=100,choices=seat_type_choices)

    def __str__(self):
        return f'{self.row_label}{self.seat_number}'
    
    
class Showtime(models.Model):
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    showtime = models.DateTimeField()
    silver_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    gold_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    recliner_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    