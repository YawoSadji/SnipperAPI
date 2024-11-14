from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


#using AbstractUser to create a custom user model here.
class User(AbstractUser):
    # id = models.AutoField(primary_key=True)
    email= models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # unique related_name
        blank=True
    )



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

#defining Snippet model here(each snippet is associated to a specific user)
class Snippet(models.Model):
    # id = models.AutoField(primary_key=True)
    language = models.CharField(max_length=25)
    code = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
            return f"{self.language} snippet by {self.owner}"