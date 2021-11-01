from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with unique email"""

    email = models.EmailField(unique=True)

        
    @property
    def user_role(self):
        if self.groups.filter(name='sale').exists():
            return 'SALE'
        elif self.groups.filter(name='support').exists():
            return 'SUPPORT'
        if self.is_superuser:
            return 'ADMIN'
