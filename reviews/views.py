from django.shortcuts import render,redirect
from .models import Review
from accounts.models import User 
from movies.models import Movie
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required
def Add_Review_view(request,slug):
    user = User.objects.get(username=request.user.username)
    if not Movie.objects.filter(slug=slug).exists():
        messages.error(request,'Invalid request')
        return redirect('/')
    movie = Movie.objects.get(slug=slug)
    if request.method == 'POST':
        rating = request.POST['rating']
        review_text = request.POST['review_text']
        Review.objects.create(user=user,movie=movie,rating=rating,review_text= review_text)
        messages.success(request,'Thanks for rating')
        return redirect(f'/movies/movie/{slug}/')
    return render(request,'reviews/add_review.html')

