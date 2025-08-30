from django.shortcuts import render,redirect
from .forms import RegisterForm,LoginForm,IdentifyForm
from django.core.mail import send_mail
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User
from django.utils import timezone 
import datetime
from .utils import get_otp,enc_uname,dec_uname
from django.contrib.auth.forms import SetPasswordForm
from django.views import View
import re
# Create your views here.

def IdentifyUserView(request):
    if request.method == 'POST':
        form = IdentifyForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                user = User.objects.get(username=username)
                otp = get_otp()
                time = timezone.now() + datetime.timedelta(minutes=10)
                user.otp = otp
                user.otp_expierd = time 
                user.otp_verified = False
                email = user.email 
                user.save()
                send_mail(
                    'OTP Verification',
                    f'Your OTP is {otp} enter otp to reset the password',
                    'support@arkcode.in',
                    [email],
                    fail_silently=False,
                )
                messages.success(request,'user found otp has sent to registerd email')
                en_uname = enc_uname(user.username)
                url = f'/accounts/verifyotp/{en_uname}/'
                return redirect(url)
            messages.error(request,'user not found')
    context = {
        'form' : IdentifyForm()
    }
    return render(request,
            'accounts/identify.html',context)
        
def OTPView(request,en_uname):
    username = dec_uname(en_uname)
    user = User.objects.get(username=username)
    if User.objects.filter(username=username).exists():
        if request.method == 'POST':
            otp1 = str(request.POST['otp1'])
            otp2 = str(request.POST['otp2'])
            otp3 = str(request.POST['otp3'])
            otp4 = str(request.POST['otp4'])
            otp =int( otp1 + otp2 + otp3 + otp4)
            
            user = User.objects.get(username=username)
            if timezone.now() <= user.otp_expierd:
                if not user.otp_verified :
                    if otp == user.otp:
                        user.otp_verified = True
                        user.save()
                        messages.success(request,'otp verified')
                        url = f'/accounts/resetpassword/{en_uname}/'
                        return redirect(url)
                    else:
                        messages.error(request,'invalid otp')
                        return redirect('identifyuser')
                messages.error(request,'otp already used')
                return redirect('identifyuser')
            messages.error(request,'otp expired')
            return redirect('identifyuser')
        context = {'user' : user,
                   'en_uname':en_uname}
        return render(request,'accounts/otp.html',context)
    messages.error(request,'invalid request')
    return redirect('login')

def ResetPasswordView(request,en_uname):
    try:
        username = dec_uname(en_uname)
    except:
        messages.error(request,'invalid request')
        return redirect('login')
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        if request.method == 'POST':
            form = SetPasswordForm(user=user,data=request.POST)
            if form.is_valid():
                messages.success(request,'password reset successful')
                form.save()
                return redirect('login')
            else:
                messages.error(request,'invalid password or password and confirm password is not matching')
        context = {
            'form' : SetPasswordForm(user=user)
        }
        return render(request,'accounts/resetpassword.html',context)
    messages.error(request,'invalid request')
    return redirect('login')

@login_required
def HomeView(request):
    return render(request,'home.html')



def LogoutView(request):
    logout(request)
    messages.error(request,'you have been logged out')
    return redirect('login')




def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_authenticated:
                    login(request, user)
                    messages.success(request,f'logged in as {username}')
                    return redirect('home')
        
    form = LoginForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)








def RegisterView(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            send_mail(
                'Registration Successfull',
                'Hello ' + fname + ' ' + lname + ',\n\nYou have successfully registered in movie ticket booking application',
                'anthonyalex543@gmail.com',
                [email],
                fail_silently=True
            )
            messages.success(request,'User account registered successfully')
            return redirect('login')
    form = RegisterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/newregister.html', context)


class ValidateUsername(View):
    def post(self,request):
        username = request.POST.get('username')
        data = {
            'is_taken': User.objects.filter(username__iexact=username).exists()
        }
        if data['is_taken']:
            data['error_message'] = 'username already taken'
            return JsonResponse(data)
        else:
            data['success_message'] = 'username is available'
            return JsonResponse(data)
        

class ValidateEmail(View):
    def post(self,request):
        email = request.POST.get('email')
        data = {
            'is_taken': User.objects.filter(email__iexact=email).exists()
        }
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if  data['is_taken']:
            data['error_message'] = 'account with this email already exists'
            return JsonResponse(data)
        elif not re.match(email_regex, email):
            return JsonResponse({"invalid_format": True,
                                 "error_message": "Enter a valid email address",
                                  "is_taken": False})
        else:
            data['success_message'] = 'email is available'
            return JsonResponse(data)
        
class ValidatePhone(View):
    def post(self,request):
        phone = request.POST.get('phone')
        data = {
            'is_taken': User.objects.filter(phone__iexact=phone).exists()
        }
        if  data['is_taken']:
            data['error_message'] = 'account with this phone number already exists'
            return JsonResponse(data)
        elif not(len(phone)==10 and str(phone)[0] >'5'):
            return JsonResponse({"invalid_format": True,
                                 "error_message": "Enter a valid phone number",
                                  "is_taken": False})
        else:
            data['success_message'] = 'phone number is available'
            return JsonResponse(data) 
        
class ValidatePassword1(View):
    def post(self,request):
        password1 = request.POST.get('password1')
        min_length = 8
        data = {}
        if len(password1) < min_length:
            data['error_message'] = f'Password must be at least {min_length} characters long.'
            data['is_valid'] = False
            return JsonResponse(data)
        if not re.search(r'[A-Z]', password1):
            data['error_message'] = 'Password must contain at least one uppercase letter.'
            data['is_valid'] = False
            return JsonResponse(data)
        if not re.search(r'[a-z]', password1):
            data['error_message'] = 'Password must contain at least one lowercase letter.'
            data['is_valid'] = False
            return JsonResponse(data)
        if not re.search(r'\d', password1):
            data['error_message'] = 'Password must contain at least one digit.'
            data['is_valid'] = False
            return JsonResponse(data)
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            data['error_message'] = 'Password must contain at least one special character.'
            data['is_valid'] = False
            return JsonResponse(data)
        data['success_message'] = 'Strong password'
        data['is_valid'] = True
        return JsonResponse(data) 
    
class ValidatePassword2(View):
    def post(self,request):
        print(request.body)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(password1)
        data = {}
        if password1 != password2:
            data['error_message'] = 'Password and Confirm Password does not match'
            data['is_valid'] = False

            return JsonResponse(data)
        else:
            data['success_message'] = 'Password and Confirm Password matched'
            data['is_valid'] = True
            return JsonResponse(data)  
    
