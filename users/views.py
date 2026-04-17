from django.shortcuts import render , HttpResponse, redirect
from django.contrib.auth import login as auth_login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import User, Client
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import CommonPasswordValidator 
import os
import random
import json
from users.utils import *
from datetime import datetime, timedelta
from django.contrib.auth.models import AnonymousUser

_CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.json')
with open(_CONFIG_PATH, "r") as file:
    CONFIG = json.load(file)

def home(request):
    return render(request, 'users/home.html')

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
                'errors': e.messages,
                'username': username,
                'email': email
            })
        
        hashed_password = make_password(password)
        user = User(username=username, email=email, password=hashed_password)   
        user.save()
        return redirect('success_register')
    return render(request, 'users/register.html')

def login(request):
    next_url = request.GET.get('next', '/user-home/')  # Redirect to intended page or home by default

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        try:
            user = User.objects.get(username=username)

            if hasattr(user, 'is_blocked') and user.is_blocked:
                return  render(request, 'users/login.html',{
                                   'error': f"{username} is blocked for a {int(CONFIG['time_to_block']/60)} minutes",
                                   })
            if user.user_check_password(password):
                user.action_count = 0

                auth_login(request, user)

                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

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

verification_codes = {}
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            verification_code = str(random.randint(100000, 999999))
            verification_codes[user.email] = verification_code
            user.save()
            request.session['user_email'] = email
            send_reset_email(user.email, verification_code)
            return redirect('write_verification_code')
        except User.DoesNotExist:
            return render(request, 'users/forgot_password.html', {'error': 'Email does not exist.'})
    return render(request, 'users/forgot_password.html')

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
            request.session['verification_code_timestamp'] = datetime.now().isoformat()
            return redirect('change_password_after_verfication_code')
        else:
            return render(request, 'users/verification_code.html', {'error': 'Invalid verfication code. Please try again.'})
    return render(request, 'users/verification_code.html')

def change_password_after_verfication_code(request):
    email = request.session.get('verified_user')
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


def user_home(request):
    return render(request, 'users/user_home.html')

def account(request):
    return render(request, 'users/account.html')

def password_policy(request):
    response = JsonResponse(CONFIG["password_policy"])
    response["Cache-Control"] = "public, max-age=3600"
    return response

def clients_page(request):
    if isinstance(request.user, AnonymousUser):
        return redirect('login')

    user = request.user

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
