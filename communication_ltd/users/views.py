from django.shortcuts import render , HttpResponse
from django.http import HttpResponse

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse

# Create your views here.
###def home(request):
###    return HttpResponse("Welcome!!!!") # בכדי להחזיר טקסט חוזר מהבקשת  HTTPS
###    #return render(request, "home.html")  #בכדי לדבר עם הHTML
###
#def register(request):
#    return render(request, 'users/register.html')

def home(request):      # # functions to call html file of home page 
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')     # maybe unite username and email 
        email = request.POST.get('email')           # such as email will be our username
        password = request.POST.get('password')

        validate_password(password)
        return HttpResponse(f"Password is valid!")  # last update

        # כאן תוכל להוסיף לוגיקה לשמירת הנתונים במסד נתונים
        return HttpResponse(f"משתמש {username} נרשם בהצלחה!")
    return render(request, 'users/register.html')

def login(request):     # functions to call html file of login page 
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
    return render(request, 'users/login.html')
