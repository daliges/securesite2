from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)  # שם המשתמש
    email = models.EmailField(unique=True)   # אימייל (ייחודי)
    password = models.CharField(max_length=128)  # סיסמה
    password_history1 = models.CharField(max_length=128, blank=True, null=True)  # סיסמה
    password_history2 = models.CharField(max_length=128, blank=True, null=True)  # סיסמה
    password_history3 = models.CharField(max_length=128, blank=True, null=True)  # סיסמה
    
    #בודק אם סיסמה גולמית תואמת לסיסמה המוצפנת
    def user_check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.name  #




