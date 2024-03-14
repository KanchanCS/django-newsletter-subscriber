from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Post, Subscription, MailMessage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text' ]
        
class RegisterForm(UserCreationForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    required_css_class = "required"

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]


class LoginForm(AuthenticationForm):
    
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )

class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            "email"
        ]
        
class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = '__all__'       