from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # our home page 
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
]