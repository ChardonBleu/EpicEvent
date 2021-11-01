from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class UserRole(models.Model):
    """user role for groups and permissions.
    """
    role = models.CharField(
        "User role",
        max_length=10,
        null=True,
        blank=True,
        help_text=_("For user role choice. Two choices possible:\
            'sale' or 'support'"),
    )

    class Meta:
        verbose_name_plural = _("User roles")

    def __str__(self):
        return "{}".format(self.role)


class CustomUser(AbstractUser):
    """Custom user model with unique email"""

    email = models.EmailField(unique=True)
    role = models.ForeignKey(
        UserRole,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="role",
        related_name="Users",
        help_text=_("Each user is related to a role. This role will attribute\
            user to a group with permissions. Roles are 'sale' or 'support'"),
    )
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print("*****", self.username, self.role)
        if self.role == 'SALE':
            sale_group = Group.objects.get(name='sale')
            print("**", sale_group)
            self.groups.add(sale_group)
        elif self.role == 'SUPPORT':
            support_group = Group.objects.get(name='support')
            print("**", support_group)
            self.groups.add(support_group)
        
    


