from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    nickname = models.CharField(max_length=24, unique=True)
    username = models.CharField(max_length=24, unique=True)
    email = models.EmailField(unique= True)
    
    first_name = None
    last_name = None
    
    class Meta:
        ordering = ['id']
    
    def __str__(self):
        return self.username