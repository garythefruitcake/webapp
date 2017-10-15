from django.contrib.auth.models import Permission, User
from django.db import models


class Profile(models.Model):
    user = models.ForeignKey(User, default=1)
    email = models.CharField(max_length=100)
    fname = models.CharField(max_length=50)
    mname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)

    def __str__(self):
        return self.lname + ' , ' + self.fname + ' ' + self.mname + '.'

class Details(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    gender = models.CharField(max_length=250)
    birthday = models.CharField(max_length=250)
    address = models.TextField()
    profile_logo = models.FileField()

    def __str__(self):
        return self.profile