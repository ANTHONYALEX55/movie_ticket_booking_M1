from django.shortcuts import render
from .models import Movie,Cast
from reviews.models import Review
from django.db.models import Avg,Count,Sum
from datetime import datetime
# Create your views here.


def MovieView(request,slug):
    movie = Movie.objects.get(slug=slug)
    casts = Cast.objects.filter(movie=movie)
    reviews = Review.objects.filter(movie=movie)
    rating = reviews.aggregate(avg=Avg('rating') )['avg']
    if (rating - int(rating)) > 0:
        rating = '{:.1f}'.format(rating)
    else :
        rating = int(rating)        
    context = {
        'movie': movie,
        'casts': casts,
        'reviews':reviews,
        'rating': rating ,
        'today' : datetime.today().date()    }
    return render(request, 'movies/movie.html', context)