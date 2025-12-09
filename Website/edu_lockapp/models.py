from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    registered_since = models.DateField(null=True, blank=True)
    last_login = models.CharField(max_length=255, null=True, blank=True)

    picture = models.ImageField(upload_to='person_pics/', null=True, blank=True, default='person_pics/default.jpg')

    def __str__(self):
        return f"Profile of {self.user.username}"
