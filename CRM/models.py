from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.db import models
from django.conf import settings


class Customer(models.Model):
    """Represents customers, with or without signed contract.
    Each customer is related to a Custom User from Sale group.
    """
    first_name = models.CharField(
        "Prénom client",
        max_length=25,
        help_text=_("Each customer has a first name with max 25 caracters."),
    )
    last_name = models.CharField(
        "Nom de famille client",
        max_length=25,
        help_text=_("Each customer has a last name with max 25 caracters.")
    )
    email = models.EmailField(
        "email client",
        max_length=100,
        help_text=_("Each customer has an email with max 100 caracters."),
    )
    phone = models.CharField(
        "Téléphone fixe client",
        max_length=20,
        help_text=_("Each customer has a phone number with max 20 caracters."),
        blank=True,
    )
    mobile = models.CharField(
        "Téléphone mobile client",
        max_length=20,
        help_text=_("Each customer has a mobile phone number with max 20 \
            caracters."),
    )
    company_name = models.CharField(
        "Company",
        max_length=250,
        help_text=_("Company name customer for professional customers with\
            max 250 caracters."),
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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Contact vendeur",
        related_name='custumers',
        help_text=_("The admin team asign a salesperson to each customer.\
            this seller negotiates with the customer for contracts sign"),
    )

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name_plural = _("Clients")

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def full_name(self):
        """return the custumer's full name"""
        return "{} {}".format(self.first_name, self.last_name.upper())


class Contract(models.Model):
    """Represents customer's contracts.
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
        help_text=_("Payment due. Format: AAAA-MM-JJ"),
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="customer",
        related_name="contracts_custumer",
        help_text=_("Each contract is related to a customer"),
    )
    sales_customuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Contact vendeur",
        related_name='contracts',
        help_text=_("The admin team asign a salesperson to each customer.\
            this seller negotiates with the customer for contracts sign"),
    )

    class Meta:
        ordering = ['customer', '-datetime_created']
        verbose_name_plural = _("Contrats")

    def __str__(self):
        return "Contracté pour {} - {} $".format(self.customer, self.amount)

    @property
    def description(self):
        """return a short dercription of contract"""
        return "Contracté pour {}".format(self.customer)


class EventStatus(models.Model):
    """Event status.
    """
    status = models.CharField(
        "Status évènement",
        max_length=250,
        help_text=_("For event status choice. Three choices\
            possibles: En préparation, En cours, Terminé"),
    )

    class Meta:
        verbose_name_plural = _("Status évènements")

    def __str__(self):
        return "{}".format(self.status)


class Event(models.Model):
    """Represents customer's event.
    Each event is related to a CustomUser from Support group
    and to a customer.
    """
    datetime_created = models.DateTimeField(
        "Date création évènement",
        auto_now_add=True,
        help_text=_("event creation datetime is automatically filled in."),
    )
    datetime_updated = models.DateTimeField(
        "Date mise à jour évènement",
        auto_now=True,
        help_text=_("event update datetime is automatically filled in."),
    )
    attendees = models.IntegerField(
        "Nombre convives",
        validators=[MinValueValidator(0)],
        null=True,
        blank=True,
        help_text=_("number of attendees. Must be positive integer"),
    )
    event_date = models.DateField(
        "Date de l'évènement",
        null=True,
        blank=True,
        help_text=_("Date event. Format: AAAA-MM-JJ"),
    )
    notes = models.TextField(
        "Notes et détails d'organisation",
        help_text=_("Notes and organisation details."),
        blank=True,
    )
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="customer",
        related_name='events_customer',
        help_text=_("Each event is related to a custumer"),
    )
    support_customuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Contact support",
        related_name='events',
        help_text=_("The admin team asign a support person to each customer.\
            this supprt personn manage event oàrganisation with the customer"),
    )
    event_status = models.ForeignKey(
        EventStatus,
        on_delete=models.CASCADE,
        verbose_name="status évènement",
        related_name='events',
        default="1",
        help_text=_("Each event has a status: '1: En préparation',\
            '2: En cours' or '3: Terminé'"),
    )

    class Meta:
        ordering = ['event_status', 'event_date']
        verbose_name_plural = _("Evènements")

    def __str__(self):
        return "Evènement commandé par {} - suivi par {}".format(
            self.customer, self.support_customuser)

    @property
    def description(self):
        """return a short description of event"""
        return "Evènement commandé par {} - suivi par {} - {} ".format(
            self.customer, self.support_customuser, self.event_status)
        
    @property
    def has_support(self):
        """Return True is event has support
        """
        if self.support_customuser == None:
            return False
        else:
            return True
        
