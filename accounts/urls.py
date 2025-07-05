from django.urls import path 
from . import views 

urlpatterns = [
    path('register/',views.RegisterView,name='register'),
    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
    path('home/',views.HomeView,name='home'),
    path('identifyuser/',views.IdentifyUserView,name='identifyuser'),
    path('verifyotp/<en_uname>/',views.OTPView,name='otp'),
    path('resetpassword/<en_uname>/',views.ResetPasswordView,name='resetpassword')
]