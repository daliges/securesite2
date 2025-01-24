from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("", views.home, name="home"),  # our home page 
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('register/success_register/', views.success_register, name='success_register'),
    path('login/change-password/', views.change_password, name='change_password'),
    path('login/forgot_password/', views.forgot_password, name='forgot_password'),
    path('login/forgot_password/write-verification-code', views.write_verification_code, name='write_verification_code'),
    path('login/forgot_password/write-verification-code/change-password', views.change_password_after_verfication_code, name='change_password_after_verfication_code'),
    path('clients/', views.clients, name='clients'),
    path('login/user-home/', views.user_home, name='user_home'),
    path('user-home/clients/', views.manage_clients, name='manage_clients'),
    path('', LogoutView.as_view(), name='logout'), # build in django function in settings
]
