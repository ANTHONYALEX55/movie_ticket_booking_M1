from django.urls import path 
from . import views 


urlpatterns = [
    path('pay/<int:booking_id>/',views.Payment_View,name='payment'),
    path('success/<int:booking_id>/',views.Success_View,name='success'),
    path('cancel/<int:booking_id>/',views.Cancel_View,name='cancel'),
]