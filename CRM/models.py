from django.utils.translation import gettext_lazy as _
from django.db import models
from accounts.models import CustomUser


class Client(models.Model):
    """Represents clients, with or without signed contract.
    Each client is related to a Custom User from Sale group.

    Arguments:
        models {[type]} -- [description]
    """
    first_name = models.CharField(
        "client first name",
        max_length=25,
        help_text=_("Each client has a first name with max 25 caracters."), 
    )
    last_name = models.CharField(
        "client last name",
        max_length=25,
        help_text=_("Each client has a last name with max 25 caracters."), 
    )
    email = models.EmailField(
        "client email",
        max_length=100,
        help_text=_("Each client has an email with max 100 caracters."), 
    )
    phone = models.CharField(
        "client phone number",
        max_length=20,
        help_text=_("Each client has a phone number with max 20 caracters."),
        blank=True, 
    )
    mobile = models.CharField(
        "client mobile phone number",
        max_length=20,
        help_text=_("Each client has a mobile phone number with max 20 \
            caracters."),
    )
    company_name = models.CharField(
        "client company name",
        max_length=250,
        help_text=_("Company name client for professional clients with max \
            250 caracters."),
        blank=True,
    )
    datetime_created = models.DateTimeField(
        "created datetime client case",
        auto_now_add=True,
        help_text=_("client creation datetime is automatically filled in."),        
    )
    datetime_updated = models.DateTimeField(
        "updated datetime client case",
        auto_now=True,
        help_text=_("client update datetime is automatically filled in."),        
    )
    sales_customuser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="sales contact",
        related_name='clients',
        help_text=_("The admin team asign a salesperson to each client.\
            this seller negotiates with the client for contracts sign"),
    )
    
    class Meta:
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        """return the client's full name"""
        return "{} {}".format(self.first_name.upper(), self.last_name)
