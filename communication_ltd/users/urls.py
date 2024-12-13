from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),  # our home page 
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('register/success_register/', views.success_register, name='success_register'),
    path('login/change-password/', views.change_password, name='change_password'),
    path('login/forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/forgot_password/write-verification-code', views.write_verification_code, name='write_verification_code')

]
