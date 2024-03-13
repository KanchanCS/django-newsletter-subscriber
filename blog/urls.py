from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path('', views.index, name='index'),
    path("add_blog", views.add_blog, name="add_blog"),
    path("details/<int:id>/", views.blog_details, name="blog_details"),
    path("edit/<int:id>/", views.edit_blog, name="edit_blog"),
    path("delete/<int:id>/", views.delete_blog, name="delete_blog"),
    path("register/", views.sign_up, name="sign_up"),
    path("logout", views.Logout, name="logout"),
    path("login", views.Login, name="login"),
    # path("Subscribe", views.blog_details, name="Subscribe"),
    
    
]