from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    age = models.CharField(max_length=8, blank=True, default="b,y,a,s")
    gender = models.CharField(max_length=3, blank=True, default="m,f")
    size = models.CharField(max_length=8, blank=True, default="s,m,l,xl")
    color = models.CharField(max_length=8, blank=True, default="d,l")

    def __str__(self):
        return self.user.username


class Dog(models.Model):
    MALE = 'm'
    FEMALE = 'f'
    GENDER_CHOICES = (
        (MALE, 'm'),
        (FEMALE, 'f'),
    )
    LIGHT = 'l'
    DARK = 'd'
    COLOR_CHOICES = (
        (LIGHT, 'l'),
        (DARK, 'd'),
    )
    name = models.CharField(max_length=255, blank=True)
    image_filename = models.CharField(max_length=500, blank=True)
    breed = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    size = models.CharField(max_length=10, blank=True)
    color = models.CharField(max_length=10, choices=COLOR_CHOICES, blank=True)

    def __str__(self):
        return self.name


class UserDog(models.Model):
    user = models.ForeignKey(User, related_query_name="usertag", on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, related_name="dogs", related_query_name="dogtag" ,on_delete=models.CASCADE)
    status = models.CharField(max_length=1, blank=True, null=True)


"""
class Company(models.Model):
    name = models.CharField(max_length=30)

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    company = models.ForeignKey(
        Company,
        related_name='employees',
        related_query_name='employee',
        on_delete=models.CASCADE,
    )
"""