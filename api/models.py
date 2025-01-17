from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    phoneNumber = models.CharField(max_length=13)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def extract_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "username": self.username,
            "phoneNumber": self.phoneNumber
        }


class Quiz(models.Model):
    topic = models.CharField(max_length=50)



