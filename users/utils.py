
import smtplib
from email.mime.text import MIMEText
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from dotenv import load_dotenv
import os
import threading

load_dotenv()
#Function that sends mails 
def send_reset_email(user_email, verification_code):
    
    body = f"Your verification code "

    message = MIMEText(verification_code)
    message["From"] = os.getenv('EMAIL_SENDER_EMAIL')
    message["To"] = user_email
    message["Subject"] = body

    try:
        with smtplib.SMTP(os.getenv('EMAIL_SERVER'), os.getenv('EMAIL_PORT')) as server:
            server.starttls()  # Secure the connection
            server.login(os.getenv('EMAIL_USERNAME'), os.getenv('EMAIL_PASSWORD'))
            server.sendmail(os.getenv('EMAIL_SENDER_EMAIL'), user_email, message.as_string())
            print("Email sent successfully!")
    except Exception as e:
        print(f"Error: {e}")

#checks if the password is correct with our validators, returns: True |  the error 
def validation_password(password):
    try:
        validate_password(password)
        return True  
    except ValidationError as e:
        return e.messages  

def user_login_management(user, time_to_block):
    user.action_count+=1
    user.save()
    if user.action_count >=3:
       user_block(user, time_to_block)

def user_block(user, time_to_block):
    if not user.is_blocked:
        user.is_blocked = True
        user.save()
        threading.Timer(time_to_block, lambda: user_unblock(user)).start()

def user_unblock(user):
    if user.is_blocked:
        user.is_blocked = False
        user.action_count = 0
        user.save()
    
            




