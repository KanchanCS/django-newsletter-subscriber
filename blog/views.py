
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    LoginForm,
    MailMessageForm,
    PostForm,
    RegisterForm,
    SubscribeForm,
)
from .models import Post


# Create your views here.
def index(request):
    post = Post.objects.all()
    paginator = Paginator(post, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html",{"page_obj": page_obj,'post':post})


def blog_details(request, id):
    
    post = get_object_or_404(Post, pk=id)       
    if request.method == "POST":
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Subscription Successful")
            return redirect('/')
    else:
        form = SubscribeForm()   
    context = {"post": post,"form":form}
    return render(request, 'details.html', context)
    
    
def delete_blog(request, id):
    if request.method == 'POST':
        pi = Post.objects.get(pk=id)
        pi.delete()
        return redirect('blog:index')
      

def edit_blog(request, id):
    pi = get_object_or_404(Post,pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=pi)
        if form.is_valid():
            form.save()
            return redirect('blog:index')  
    else:
        form = PostForm(instance=pi)        
    return render(request, 'edit_blog.html', {'form':form})    

        
def add_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  
        if form.is_valid():
            title= form.cleaned_data['title']
            text= form.cleaned_data['text']
         
            post = Post( title=title, text=text)
            post.save()
            
            form = PostForm()  # Clear the form
            return redirect("blog:index")
    else:
            form = PostForm()            
    return render(request, "add_blog.html", {'form': form})   


def sign_up(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

        login(request, user)
        return redirect("blog:login")
    else:
        form = RegisterForm()

    context = {
        "form": form,
    }
    return render(request, "register.html", context)


def Login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return redirect("blog:index")

    else:
        form = LoginForm()

    context = {"forms": form}
    return render(request, "login.html", context)


def Logout(request):
    logout(request)
    return redirect("blog:index")   

def mail_letter(request):
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data.get('title')
            message = form.cleaned_data.get('message')
            send_mail(
            title,
            message,
            'imkanchan7422@gmail.com',
            ["erkanchan016@gmail.com"],
            fail_silently=False,
            )
            messages.success(request, 'Message has been sent to Mail List')
            return redirect('blog:mail_letter')
    else:
        form = MailMessageForm()        
    context = {
        'form':form
    }
    return render(request, 'mail_letter.html',context)  