from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Account(models.Model):
    class Currency(models.TextChoices):
        USD = 'USD', _('US dollar')
        CAD = 'CAD', _('CA dollar')
        
    name = models.CharField(max_length=100)
    currency_code = models.CharField(max_length=3, choices=Currency.choices, default=Currency.CAD)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + " (" + self.owner.username + ")"
            
class CreditCard(models.Model):
    name = models.CharField(max_length=50)
    application_date = models.DateField(null=True, blank=True)
    deadline_minimum_spending = models.DateField(null=True, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    cancellation_date = models.DateField(null=True, blank=True)
    mininum_spending = models.IntegerField(null=True, blank=True)
    signup_bonus = models.IntegerField(null=True, blank=True)
    first_year_fee = models.DecimalField(max_digits=10, decimal_places=2)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2)
    cycle_day = models.IntegerField(null=True, blank=True)
    earning_rates = models.CharField(max_length=200, null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + " (" + self.owner.username + ")"

class Category(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name + " (" + self.owner.username + ")"
    
class Expense(models.Model):
    class PaymentMethodType(models.TextChoices):
        CREDIT_CARD = 'CC', _('Credit card')
        CASH = 'CA', _('Cash')
        ETRANSFER = 'ET', _('E transfer')
        DIRECT_TRANSFER = 'TR', _('Direct transfer')
        CHECK = 'CK', _('Check')
        
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateField()
    payment_method_type = models.CharField(max_length=2,
        choices=PaymentMethodType.choices,
        default=PaymentMethodType.CREDIT_CARD,
    )
    credit_card = models.ForeignKey('CreditCard', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)
    account = models.ForeignKey('Account', on_delete=models.CASCADE)