from django.urls import path 
from . import views 

urlpatterns = [
    path('', views.home, name='home'),
    path('yourorders/',views.YourOrders_View,name='yourorders'),
    path('search/',views.SearchView,name='search')
]