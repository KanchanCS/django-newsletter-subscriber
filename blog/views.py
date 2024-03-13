from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LoginForm, PostForm, RegisterForm, SubscribeForm
from .models import Post, Subscription


# Create your views here.
def index(request):
    post = Post.objects.all()
    paginator = Paginator(post, 3)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html",{"page_obj": page_obj,'post':post})


def blog_details(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            post = get_object_or_404(Post, pk=id)
            form = SubscribeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = SubscribeForm()   
            context = {"post": post,"form":form}
        return render(request, 'details.html', context)
    else:
        return redirect('blog:login')
    
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


