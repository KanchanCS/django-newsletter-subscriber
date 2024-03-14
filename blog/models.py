from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
    
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True,
            blank=True, null=True)

    def __str__(self):
        return self.title
    


class Subscription(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email   
    
class MailMessage(models.Model):
    title = models.CharField(max_length=150,null=True)
    message = models.TextField(null=True)
    
    def __str__(self):
        return self.title
       
    
    
    
    