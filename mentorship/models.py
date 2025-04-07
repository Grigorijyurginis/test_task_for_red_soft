from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Username and password are required, other fields are optional by AbstractUser
    """
    phone = models.CharField(max_length=15, blank=True, null=True)
    mentor = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='mentees',
        on_delete=models.SET_NULL
    )

    @property
    def is_mentor(self):
        return self.mentees.exists()

    def __str__(self):
        return self.username
