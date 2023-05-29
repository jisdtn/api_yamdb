from django.contrib.auth.models import AbstractUser
from django.db import models


USER_ROLES = (
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
)


class User(AbstractUser):
    bio = models.TextField(
        'Bio',
        blank=True,
    )

    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
        default='user',
    )
