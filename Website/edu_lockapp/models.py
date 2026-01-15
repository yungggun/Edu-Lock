from django.db import models
from django.contrib.auth.models import User
import hashlib
from django.conf import settings


class ClassGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    uid_hash = models.CharField(
        max_length=128,
        unique=True,
        null=True,
        blank=True
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='student'
    )

    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_blocked = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)

    registered_since = models.DateField(
        auto_now_add=True,
        null=True,
        blank=True
    )

    picture = models.ImageField(
        upload_to='person_pics/',
        default='person_pics/default.jpg',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    def generate_uid(self, raw_uid: str):
        secret = settings.SECRET_KEY
        self.uid_hash = hashlib.sha256(
            f"{raw_uid}{secret}".encode()
        ).hexdigest()


class Doors(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    device_id = models.CharField(max_length=100, unique=True)

    class_group = models.ForeignKey(
        ClassGroup,
        on_delete=models.CASCADE
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='offline'
    )

    is_locked = models.BooleanField(default=True)

    def __str__(self):
        return f"Kasten {self.device_id} ({self.status})"


class Log(models.Model):
    LOG_TYPES = [
        ("Zugriff", "Zugriff"),
        ("Fehler", "Fehler"),
    ]

    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=LOG_TYPES)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    source = models.CharField(max_length=100, default="SYSTEM")

    def __str__(self):
        return f"[{self.type}] {self.message}"

