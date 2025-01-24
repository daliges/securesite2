from django.shortcuts import render , HttpResponse, redirect
from django.http import HttpResponse
from django.core.exceptions import ValidationError

def system_page(request):      # # functions to call html file of home page 
    return render(request, 'users/user_home.html')

def account(request):
    return render(request, 'users/account.html')