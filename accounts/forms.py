from django import forms 
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm)
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email', 
                  'phone', 'password1', 'password2')
        
    def clean_password1(self):
        password = self.cleaned_data['password1']
        u,l,s,d =0,0,0,0
        for i in password:
            if i.isupper():
                u =1
            elif i.islower():
                l =1
            elif i.isdigit():
                d =1
            else:
                s =1
        if u and l and s and d and len(password)>=8:
            return password
        else:
            raise forms.ValidationError("Password must contain at least one uppercase letter, one lowercase letter, one digit, one special character and must be at least 8 characters long.")
    
    
        
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    class Meta:
        model = User
    
        

class IdentifyForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))