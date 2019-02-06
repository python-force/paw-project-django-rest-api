from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    dog_age = models.CharField(max_length=3, blank=True, default="b,y,a,s")
    dog_gender = models.CharField(max_length=8, blank=True, default="m,f")
    dog_size = models.CharField(max_length=8, blank=True, default="s,m,l,xl")


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=500)
    breed = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=1)

    def __str__(self):
        return self.name

