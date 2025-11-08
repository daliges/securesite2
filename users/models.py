from django.db import models
from django.contrib.auth.hashers import check_password

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import check_password

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        
        # Validate email
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Invalid email format")
        
        # Sanitize username (remove leading/trailing spaces)
        username = username.strip()

        # Validate username format (allowed characters: letters, numbers, @, ., _, -)
        if not re.match(r'^[a-zA-Z0-9@._-]+$', username):
            raise ValidationError("Invalid characters in username")
        
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)  
    email = models.EmailField(unique=True)  
    password = models.CharField(max_length=128)  
    password_history1 = models.CharField(max_length=128, blank=True, null=True)  
    password_history2 = models.CharField(max_length=128, blank=True, null=True)  
    password_history3 = models.CharField(max_length=128, blank=True, null=True)  
    is_blocked = models.BooleanField(default=False)  
    action_count = models.IntegerField(default=0)  # num of tries to login
    last_login = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=150, default='Unknown')  # Added to fix __str__ issue

    # Define authentication fields
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    # בודק אם סיסמה גולמית תואמת לסיסמה המוצפנת
    def user_check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username


class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client",max_length=100)
    client_id = models.CharField(max_length=20,unique=True)
    client_name = models.CharField(max_length=100)
    client_address = models.TextField()
    
    def __str__(self): 
        return self.client_name



