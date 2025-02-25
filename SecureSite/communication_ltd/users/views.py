from django.shortcuts import render , HttpResponse, redirect
from django.contrib.auth import login as auth_login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User, Client
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import CommonPasswordValidator 
import random
import json
from users.utils import *
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser


with open(r"communication_ltd/config.json", "r") as file:
    CONFIG = json.load(file)

# functions to call html file of home page
def home(request):       
    return render(request, 'users/home.html')

# page of registeration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')     
        email = request.POST.get('email')           
        password = request.POST.get('password')
        if  User.objects.filter(username=username).exists():
            return render(request,'users/register.html',
                          {
                              'errors': ["username is allready use."],
                              'username': username,
                              'email':email
                      })
        if  User.objects.filter(email=email).exists():
            return render(request,'users/register.html',
                          {
                              'errors': ["Email is allready use."],
                              'username': username,
                              'email':email
                      })
        
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, 'users/register.html', {
                'errors': e.messages,  # Pass validation error messages to the template
                'username': username,
                'email': email
            })
        
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password)   
        user.save()
        return redirect('success_register')
    return render(request, 'users/register.html')

# page of login 
def login(request):
    next_url = request.GET.get('next', '/user-home/')  # Redirect to intended page or home by default

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = User.objects.get(username=username)

            if hasattr(user, 'is_blocked') and user.is_blocked: # added hasattr to handle 2 cases
                return  render(request, 'users/login.html',{
                                   'error': f"{username} is blocked for a {int(CONFIG['time_to_block']/60)} minutes",
                                   })
            if user.user_check_password(password):
                user.action_count = 0

                # Authenticate and log in the user using Django's session framework
                auth_login(request, user)

                # Remember Me logic
                if remember_me:
                    request.session.set_expiry(1209600)  # 2 weeks
                else:
                    request.session.set_expiry(0)  # Expire on browser close

                # Redirect the user accordingly
                return HttpResponseRedirect(request.POST.get('next', next_url))
            else:
                user_login_management(user,CONFIG['time_to_block'])
                return render(request, 'users/login.html',{
                                   'error': f"User or Password does not exist.You have {3 - user.action_count} attempts.",
                                   'username': username
                                   }) 
        except User.DoesNotExist:
            return render(request, 'users/login.html', {'error': "User or Password does not exist"})
    return render(request, 'users/login.html', {'next': next_url})

# page of succession    
def success_register(request):
    return render(request, 'users/success_register.html')


# page of changing password by username and current password 
def change_password(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        retype_new_password = request.POST.get("retype_new_password")
        try:
            user = User.objects.get(username=username)
            if user.is_blocked:
                return  render(request, 'users/change_password.html',{
                                   'errors': [f"{username} is blocked for a {int(CONFIG['time_to_block']/60)} minutes"],
                                   })
            if user.user_check_password(current_password):
                user.action_count = 0
                password_history = [
                    user.password_history1,
                    user.password_history2,
                    user.password_history3,
                ]
                for old_password in password_history:
                    if old_password and check_password(new_password, old_password):
                        return render(request, 'users/change_password.html',
                                      {
                                          'errors': ['The new password can\'t be the same as any of the last 3 passwords.'],
                                          'username': username,
                                          'current_password': current_password
                                          })
                password_check = validation_password(new_password)
                if password_check is not True:
                    return render(request, 'users/change_password.html',
                                  {
                                      'errors': password_check,
                                      'username': username,
                                      'current_password': current_password
                                      })
                if user.user_check_password(new_password):
                     return render(request, 'users/change_password.html', 
                                   {
                                       'errors': ["You entered the same password as your old password."],
                                       'username': username,
                                       'current_password': current_password
                                         })
                if new_password != retype_new_password:
                    return render(request, 'users/change_password.html', 
                                  {
                                      'errors': ["The new password you entered does not match the password you are repeating."],
                                      'username': username,
                                      'current_password': current_password
                                      })
                
                user.password_history3 = user.password_history2
                user.password_history2 = user.password_history1
                user.password_history1 = user.password
                user.password = make_password(new_password)
                user.save()
                # return HttpResponse(f"password of {username} changed successfuly")
                return redirect('success_register')
            else:
                user_login_management(user,CONFIG['time_to_block'])
                return render(request, 'users/change_password.html',{
                                   'errors': [f"User or Password does not exist.You have {3 - user.action_count} attempts."],
                                   'username': username
                                   }) 
        except User.DoesNotExist:
            return render(request, 'users/change_password.html', {'errors': ["User or password does not exist"]})
    return render(request, 'users/change_password.html') 

# page of forgot password | get the email for verfication 
verification_codes = {}
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_verification_code = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a verification code
            verification_code = str(random.randint(100000, 999999)) 
            # Save the code to the user (אופציונלי)
            verification_codes[user.email] = verification_code
            user.save()
            # Send email
            request.session['user_email'] = email
            send_reset_email(user.email, verification_code)
            return redirect('write_verification_code')
            #return render(request, 'users/verification_code.html', {'success': 'Verification code sent to your email.'})
        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {'error': 'Email does not exist.'})
    return render(request, 'users/forgot_password.html')

# page of verfication by verfication code that sent to the email
def write_verification_code(request):
    if request.method == 'POST':
        verification_code = request.POST.get('verification_code')
        email = request.session.get('user_email')
        if not email:
            return render('users/forgot_password.html', {'error': 'Session expired. Please try again.'})
        expected_code = verification_codes.get(email)
        if expected_code and verification_code == expected_code:
            del verification_codes[email]
            request.session['verified_user'] = email
            request.session['verification_code_verified'] = True
            request.session['verification_code_timestamp'] = datetime.now().isoformat()  # שמור זמן יצירת האימות
            request.session['verified_user'] = email
            return redirect('change_password_after_verfication_code')
        else:
            return render(request, 'users/verification_code.html', {'error': 'Invalid verfication code. Please try again.'})
    return render(request, 'users/verification_code.html')

 # page of changing password by verfication email by verfication code
def change_password_after_verfication_code(request):
    email = request.session.get('verified_user')  # בדוק אם המשתמש אומת
    verification_verified = request.session.get('verification_code_verified')
    code_time = request.session.get('verification_code_timestamp')
    if not email or not verification_verified or not code_time:  
        return redirect('forgot_password')
    
    if datetime.fromisoformat(code_time) + timedelta(minutes=5) < datetime.now():
        del request.session['verified_user']
        del request.session['verification_code_verified']
        del request.session['verification_code_timestamp']
        return redirect('forgot_password')
    
    if request.method == 'POST':
        new_password = request.POST.get("new_password")
        retype_new_password = request.POST.get("retype_new_password")
        try:
            user = User.objects.get(email=email)
            password_history = [
                user.password_history1,
                user.password_history2,
                user.password_history3,
            ]
            for old_password in password_history:
                if old_password and check_password(new_password, old_password):
                    return render(request, 'users/change_password_after_verification_code.html',
                                    {
                                      'errors': ['The new password can\'t be the same as any of the last 3 passwords.']
                                      })
            password_check = validation_password(new_password)
            if password_check is not True:
                return render(request, 'users/change_password_after_verification_code.html', {'errors': password_check})
            
            if new_password != retype_new_password:
                return render(request, 'users/change_password_after_verification_code.html', {'errors': ["The new password you entered does not match the password you are repeating."]})
            user.password_history3 = user.password_history2
            user.password_history2 = user.password_history1
            user.password_history1 = user.password
            user.password = make_password(new_password)
            user.save()
            del request.session['verified_user']
            del request.session['verification_code_verified']
            del request.session['verification_code_timestamp']
            
            return redirect('success_register')
        except User.DoesNotExist:
            return render(request, 'users/change_password_after_verification_code.html', {'errors': ["User does not exist"]})
    return render(request, 'users/change_password_after_verification_code.html')


def user_home(request):      # # functions to call html file of home page 
    return render(request, 'users/user_home.html')

def account(request):
    return render(request, 'users/account.html')

def clients_page(request):
    
    # Ensure the user is authenticated before proceeding
    if not request.user or isinstance(request.user, AnonymousUser):
        return redirect('login')

    user = request.user  # Now safe to use as user is authenticated 

    if request.method == 'POST':
        if 'delete_client' in request.POST:
            client_id = request.POST.get('delete_client')
            Client.objects.filter(user=user, client_id=client_id).delete()
        else:
            client_name = request.POST.get('client_name')
            client_address = request.POST.get('client_address')

            if client_name and client_address:
                client_id = f"CL-{random.randint(1000, 9999)}"
                client = Client(user=user, client_id=client_id, client_name=client_name, client_address=client_address)
                client.save()

    clients = Client.objects.filter(user=user)
    return render(request, 'users/clients_page.html', {'clients': clients}) 
