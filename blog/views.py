
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import MailMessageForm, PostForm, SubscribeForm
from .models import Post, Subscription


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




def add_blog(request):
  if request.method == 'POST':
    form = PostForm(request.POST, request.FILES)
    if form.is_valid():
      title = form.cleaned_data['title']
      text = form.cleaned_data['text']

      post = Post(title=title, text=text)
      post.save()

      # Get all subscribed users (assuming a Subscriber model)
      subscribers = Subscription.objects.all()

      # Construct the email message
      subject = f"New Blog Post: {title}"
      message = f"A new blog post titled '{title}' has been published! Check it out here: http://127.0.0.1:8000/{reverse('blog:blog_details', kwargs={'id': post.pk})}"

      # Send email to all subscribers
      for subscriber in subscribers:
        # send_mail(
        #   subject,
        #   message,
        #   'imkanchan7422@gmail.com',  # Replace with your email address
        #   [subscriber.email],
        #   fail_silently=False,
        # )
        pass
      form = PostForm()  # Clear the form
      return redirect("blog:index")
  else:
    form = PostForm()
  return render(request, "add_blog.html", {'form': form})
 


def mail_letter(request):
    if request.method == 'POST':
        form = MailMessageForm(request.POST)
        if form.is_valid():
            form.save()
            title = form.cleaned_data['title']
            message = form.cleaned_data['message']
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


