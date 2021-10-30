from django.utils.translation import gettext_lazy as _
from django.db import models
from accounts.models import CustomUser


class Custumer(models.Model):
    """Represents custumers, with or without signed contract.
    Each custumer is related to a Custom User from Sale group.

    """
    first_name = models.CharField(
        "Prénom client",
        max_length=25,
        help_text=_("Each custumer has a first name with max 25 caracters."), 
    )
    last_name = models.CharField(
        "Nom de famille client",
        max_length=25,
        help_text=_("Each custumer has a last name with max 25 caracters."), 
    )
    email = models.EmailField(
        "email client",
        max_length=100,
        help_text=_("Each custumer has an email with max 100 caracters."), 
    )
    phone = models.CharField(
        "Téléphone fixe client",
        max_length=20,
        help_text=_("Each custumer has a phone number with max 20 caracters."),
        blank=True, 
    )
    mobile = models.CharField(
        "Téléphone mobile client",
        max_length=20,
        help_text=_("Each custumer has a mobile phone number with max 20 \
            caracters."),
    )
    company_name = models.CharField(
        "Company",
        max_length=250,
        help_text=_("Company name custumer for professional custumers with max \
            250 caracters."),
        blank=True,
    )
    datetime_created = models.DateTimeField(
        "Date création client",
        auto_now_add=True,
        help_text=_("custumer creation datetime is automatically filled in."),        
    )
    datetime_updated = models.DateTimeField(
        "Date mise à jour client",
        auto_now=True,
        help_text=_("custumer update datetime is automatically filled in."),        
    )
    sales_customuser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Contact vendeur",
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


class Contract(models.Model):
    """Represents custumer's contracts.
    Each contract is related to a Custom User from Sale group
    and to a custumer.

    """
    datetime_created = models.DateTimeField(
        "Date création contrat",
        auto_now_add=True,
        help_text=_("contract creation datetime is automatically filled in."),        
    )
    datetime_updated = models.DateTimeField(
        "Date mise à jour contrat",
        auto_now=True,
        help_text=_("contract update datetime is automatically filled in."),        
    )
    status_sign = models.BooleanField(
        "Signature contrat",
        default=False,
        help_text=_("Has to pass on True when contract is signed"), 
    )
    amount = models.DecimalField(
        "Montant du contrat",
        max_digits=9,
        decimal_places=2,
        help_text=_("Contract amount when signed. Float number"),
    )
    payment_due = models.DateField(
        "Echéance de paiement",
        help_text=_("Payment due. Format:  AAAA-MM-JJ"),
    )
    custumer = models.ForeignKey(
        Custumer,
        on_delete=models.CASCADE,
        verbose_name="client",
        related_name="contracts_custumer",
        help_text=_("Each contract is related to a custumer"),
    )
    sales_customuser = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name="Contact vendeur",
        related_name='contracts',
        help_text=_("The admin team asign a salesperson to each custumer.\
            this seller negotiates with the custumer for contracts sign"),
    )
    
    class Meta:
        ordering = ['custumer', '-datetime_created']
    
    def __str__(self):
        return "Contracté pour {} - {} $".format(self.custumer, self.amount)
    
    @property
    def description(self):
        """return the custumer's full name"""
        return "Contracté pour {}".format(self.custumer)