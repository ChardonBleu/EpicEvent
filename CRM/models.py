from django.utils.translation import gettext_lazy as _
from django.db import models
from accounts.models import CustomUser


class Custumer(models.Model):
    """Represents custumers, with or without signed contract.
    Each custumer is related to a Custom User from Sale group.

    Arguments:
        models {[type]} -- [description]
    """
    first_name = models.CharField(
        "custumer first name",
        max_length=25,
        help_text=_("Each custumer has a first name with max 25 caracters."), 
    )
    last_name = models.CharField(
        "custumer last name",
        max_length=25,
        help_text=_("Each custumer has a last name with max 25 caracters."), 
    )
    email = models.EmailField(
        "custumer email",
        max_length=100,
        help_text=_("Each custumer has an email with max 100 caracters."), 
    )
    phone = models.CharField(
        "custumer phone number",
        max_length=20,
        help_text=_("Each custumer has a phone number with max 20 caracters."),
        blank=True, 
    )
    mobile = models.CharField(
        "custumer mobile phone number",
        max_length=20,
        help_text=_("Each custumer has a mobile phone number with max 20 \
            caracters."),
    )
    company_name = models.CharField(
        "custumer company name",
        max_length=250,
        help_text=_("Company name custumer for professional custumers with max \
            250 caracters."),
        blank=True,
    )
    datetime_created = models.DateTimeField(
        "created datetime custumer case",
        auto_now_add=True,
        help_text=_("custumer creation datetime is automatically filled in."),        
    )
    datetime_updated = models.DateTimeField(
        "updated datetime custumer case",
        auto_now=True,
        help_text=_("custumer update datetime is automatically filled in."),        
    )
    sales_customuser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="sales contact",
        related_name='custumers',
        help_text=_("The admin team asign a salesperson to each custumer.\
            this seller negotiates with the custumer for contracts sign"),
    )
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        """return the custumer's full name"""
        return "{} {}".format(self.first_name, self.last_name.upper())
