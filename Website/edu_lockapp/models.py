from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  

    firstname = models.CharField(max_length=30, default='Max')
    lastname = models.CharField(max_length=30, default='Mustermann')

    def __str__(self):
        return f"{self.user.username} - {self.firstname} {self.lastname}"