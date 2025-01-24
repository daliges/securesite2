from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)  # שם המשתמש
    email = models.EmailField(unique=True)   # אימייל (ייחודי)
    password = models.CharField(max_length=128)  # סיסמה
    password_history1 = models.CharField(max_length=128, blank=True, null=True)  # סיסמה
    password_history2 = models.CharField(max_length=128, blank=True, null=True)  # סיסמה
    password_history3 = models.CharField(max_length=128, blank=True, null=True)  # סיסמה
    is_blocked = models.BooleanField(default=False)  # if the user is blocked
    action_count = models.IntegerField(default=0) #nun of try to login
    #בודק אם סיסמה גולמית תואמת לסיסמה המוצפנת
    def user_check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
    def __str__(self):
        return self.name  #

class Client(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client",max_length=100)
    client_id = models.CharField(max_length=20,unique=True)
    client_name = models.CharField(max_length=100)
    client_address = models.TextField()
    client_created_at = models.DateTimeField(auto_now_add=True)
    client_tpdated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.client_id}" 



