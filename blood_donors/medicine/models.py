from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=10)
    birthday = models.DateTimeField()
    role = models.CharField(max_length=50,default="client")
    exp = models.FloatField(default=0.0)

    def __str__(self):
        return self.user.username
