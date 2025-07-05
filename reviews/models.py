from django.db import models
from accounts.models import User 
from movies.models import Movie
# Create your models here.

class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3,decimal_places=1,null=True,blank=True)
    review_text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
