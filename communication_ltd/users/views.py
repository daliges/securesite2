from django.shortcuts import render , HttpResponse, redirect
from django.http import HttpResponse

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import User
from django.contrib.auth.hashers import make_password

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

        password_check = validation_password(password)
        if password_check is not True:
            return render(request, 'users/register.html',
                      {
                          'errors': password_check,
                          'username': username,
                          'email':email
                      })
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password)   #שמירת יוזרים עדיין לא בוצע
        user.save()
        return redirect('success_register')
    return render(request, 'users/register.html')

def login(request):     # functions to call html file of login page 
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        ####עדיין לא נבדק לכאן הוספתי לוגיקה אם המשתמש קיים
        ###try:
        ###    user = User.objects.get(username=username)
        ###    if user.password == password:
        ###        return HttpResponse(f"{username} login successfuly")
        ###    else:
        ###        return render(request, 'users/login.html', {'error': "Invalid password"}) #להוסיף מה יקרה כאשר שם המשתמש או הסיסמא לא קיימים
        ###except User.DoesNotExist:
        ###    return render(request, 'users/login.html', {'error': "User does not exist"})
    return render(request, 'users/login.html')

def validation_password(password):
    try:
        # פונקציה מובנית ב-Django לאימות סיסמאות מתוך קובץ ה-settings
        validate_password(password)
        return True  # מחזיר 1 אם הסיסמה תקינה
    except ValidationError as e:
        return e.messages  # מחזיר את רשימת ההודעות במקרה של שגיאה
    
def success_register(request):
    return render(request, 'users/success_register.html')