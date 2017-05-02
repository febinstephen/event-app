from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(User)
    picture = models.ImageField(blank=True)

    def __str__(self):
        return self.user.username


class Event(models.Model):

    name = models.CharField(max_length=40)
    date = models.DateField(blank=False)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.name
