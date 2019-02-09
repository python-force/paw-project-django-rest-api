from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    age = models.CharField(max_length=8, blank=True, default="b,y,a,s")
    gender = models.CharField(max_length=3, blank=True, default="m,f")
    size = models.CharField(max_length=8, blank=True, default="s,m,l,xl")

    def __str__(self):
        return self.user.username


class Dog(models.Model):
    name = models.CharField(max_length=255, blank=True)
    image_filename = models.CharField(max_length=500, blank=True)
    breed = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(blank=True)
    gender = models.CharField(max_length=10, blank=True)
    size = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, blank=True, null=True)