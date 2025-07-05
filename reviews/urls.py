from django.urls import path 
from . import views 

urlpatterns = [
    path('add_review/<slug>/',views.Add_Review_view,name='add_review')
]