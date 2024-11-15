from django.db import models
###########################################עצרו פה
from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)  # שם המשתמש
    email = models.EmailField(unique=True)   # אימייל (ייחודי)
    password = models.CharField(max_length=128)  # סיסמה

    def __str__(self):
        return self.name  #




