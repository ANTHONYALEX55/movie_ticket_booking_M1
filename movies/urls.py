from django.urls import path 
from . import views 

urlpatterns = [
    path('movie/<slug>/',views.MovieView,name='movie')
]