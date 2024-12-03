from django.db import models
###########################################עצרו פה

class User(models.Model):
    name = models.CharField(max_length=100, unique=True)  # שם המשתמש
    email = models.EmailField(unique=True)   # אימייל (ייחודי)
    password = models.CharField(max_length=128)  # סיסמה

    def __str__(self):
        return self.name  #




