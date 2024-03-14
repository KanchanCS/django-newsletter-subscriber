from django import forms
from .models import Post, Subscription, MailMessage


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','text' ]
        


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