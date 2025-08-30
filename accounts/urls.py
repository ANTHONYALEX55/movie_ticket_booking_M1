from django.urls import path 
from . import views 
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register/',views.RegisterView,name='register'),
    path('login/',views.LoginView,name='login'),
    path('logout/',views.LogoutView,name='logout'),
    path('home/',views.HomeView,name='home'),
    path('identifyuser/',views.IdentifyUserView,name='identifyuser'),
    path('verifyotp/<en_uname>/',views.OTPView,name='otp'),
    path('resetpassword/<en_uname>/',views.ResetPasswordView,name='resetpassword'),
    path('validateusername/',csrf_exempt(views.ValidateUsername.as_view()),name='validateusername'),
    path('validateemail/',csrf_exempt(views.ValidateEmail.as_view()),name='validateemail'),
    path('validatephone/',csrf_exempt(views.ValidatePhone.as_view()),name='validatephone'),
    path('validatepassword/',csrf_exempt(views.ValidatePassword1.as_view()),name='validatepassword1'),
    path('validatepassword2/',csrf_exempt(views.ValidatePassword2.as_view()),name='validatepassword2'),
]