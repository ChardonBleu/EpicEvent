from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Custom user model with unique email"""

    email = models.EmailField(unique=True)

    @property
    def user_role(self):
        is_in_sale_goup = self.groups.filter(name='sale').exists()
        is_in_support_group = self.groups.filter(name='support').exists()
        if self.is_superuser:
            return 'ADMIN'
        elif is_in_sale_goup and is_in_support_group:
            return 'ERROR'
        elif is_in_sale_goup:
            return 'SALE'
        elif is_in_support_group:
            return 'SUPPORT'
        else:
            return 'Inconnu'
