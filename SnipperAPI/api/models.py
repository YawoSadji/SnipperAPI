from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


#using AbstractUser to create a custom user model here.
class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=255)

#defining Snippet model here(each snippet is associated to a specific user)
class Snippet(models.Model):
    id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=25)
    code = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
