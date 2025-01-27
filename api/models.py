from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import TextField
from scipy.signal import max_len_seq


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
    quiz_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    access_link = models.URLField(max_length=200, default='https://default-link.com')
    quiz_name = models.CharField(max_length=50)



    def __str__(self):
        return self.quiz_name


class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE) # Many to one
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=20)
    multiple = models.BooleanField(default=False)
    required = models.BooleanField(default=False)


    def __str__(self):
        return self.question_id


class Answers(models.Model):
    ans_id = models.AutoField(primary_key=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # Many to one
    answer = models.TextField(max_length=200)
    state = models.BooleanField(default=False)


    def __str__(self):
        return self.ans_id


