from django.shortcuts import render , HttpResponse, redirect
from django.http import HttpResponse

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from .models import User
from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail
#from django.contrib.auth.models import User
import random
import json

# Create your views here.
###def home(request):
###    return HttpResponse("Welcome!!!!") # בכדי להחזיר טקסט חוזר מהבקשת  HTTPS
###    #return render(request, "home.html")  #בכדי לדבר עם הHTML
###
#def register(request):
#    return render(request, 'users/register.html')

with open(r"communication_ltd/config.json", "r") as file:
    CONFIG = json.load(file)

def home(request):      # # functions to call html file of home page 
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')     # maybe unite username and email 
        email = request.POST.get('email')           # such as email will be our username
        password = request.POST.get('password')

        if  User.objects.filter(email=email).exists():
            return render(request,'users/register.html',
                          {
                              'errors': ["Email is allready use."],
                              'username': username,
                              'email':email
                      })

        password_check = validation_password(password)
        if password_check is not True:
            return render(request, 'users/register.html',
                      {
                          'errors': password_check,
                          'username': username,
                          'email':email
                      })
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password)   
        user.save()
        return redirect('success_register')
    return render(request, 'users/register.html')

def login(request):     # functions to call html file of login page 
    if request.method == 'POST':
        username = request.POST.get('username')
        #email = request.POST.get('email')
        password = request.POST.get('password')
        #עדיין לא נבדק לכאן הוספתי לוגיקה אם המשתמש קיים
        try:
            user = User.objects.get(username=username)
            if user.user_check_password(password):
                return HttpResponse(f"{username} login successfuly")
            else:
                return render(request, 'users/login.html', {'error': "Invalid password"}) #להוסיף מה יקרה כאשר שם המשתמש או הסיסמא לא קיימים
        except User.DoesNotExist:
            return render(request, 'users/login.html', {'error': "User does not exist"})
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



def change_password(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        retype_new_password = request.POST.get("retype_new_password")
        try:
            user = User.objects.get(username=username)
            if user.user_check_password(current_password):
                password_check = validation_password(new_password)
                if password_check is not True:
                    return render(request, 'users/change_password.html',
                                  {
                                      'errors': password_check,
                                      })
                if user.user_check_password(new_password):
                     return render(request, 'users/change_password.html', {'errors': ["You entered the same password as your old password."]})
                if new_password != retype_new_password:
                    return render(request, 'users/change_password.html', {'errors': ["The new password you entered does not match the password you are repeating."]})
                user.password = make_password(new_password)
                user.save()
                return HttpResponse(f"password of {username} changed successfuly")
            else:
                return render(request, 'users/change_password.html', {'errors': ["Invalid password"]})
        except User.DoesNotExist:
            return render(request, 'users/change_password.html', {'errors': ["User does not exist"]})
    return render(request, 'users/change_password.html') 



def send_reset_email(user_email, verification_code):
    email_settings = CONFIG['email_settings']
    send_mail(
        email_settings["subject_line"],
        f'Your verification code is: {verification_code}',  # Message body
        email_settings["username"],
        [user_email],  # To email
        fail_silently=False,
    )


verification_codes = {}

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a verification code
            verification_code = str(random.randint(100000, 999999)) 
            # Save the code to the user (אופציונלי)
            verification_codes[user.email] = verification_code
            user.save()
            # Send email
            send_reset_email(user.email, verification_code)
            return render(request, 'users/forgot_password.html', {'success': 'Verification code sent to your email.'})
        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {'error': 'Email does not exist.'})
    return render(request, 'users/forgot_password.html')


#            
#            return render(request, 'users/forgot_password.html', {
#                'success': 'Verification code sent to your email.',
#                'email': email,
#            })
#        except User.DoesNotExist:
#            return render(request, 'users/forgot_password.html', {
#                'error': 'No account found with that email.'
#            })
#
#    return render(request, 'users/forgot_password.html')
