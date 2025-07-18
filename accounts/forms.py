from django import forms 
from django.contrib.auth.forms import (UserCreationForm,
                                       AuthenticationForm)
from .models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email', 
                  'phone', 'password1', 'password2')
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter Username'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter Password'})}
        

class IdentifyForm(forms.Form):
    username = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter Username'}))