from factory.django import DjangoModelFactory
from . import models

class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = 'John'
    last_name = 'Doe'


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = models.Account

    name = 'Main'
    currency_code = 'CAD'
    
class CreditCardFactory(DjangoModelFactory):
    class Meta:
        model = models.CreditCard
    
    name = 'Visa'
    # application_date = models.DateField(null=True, blank=True)
    # deadline_minimum_spending = models.DateField(null=True, blank=True)
    # approval_date = models.DateField(null=True, blank=True)
    # cancellation_date = models.DateField(null=True, blank=True)
    minimum_spending = 1000
    signup_bonus = 25000
    first_year_fee = 0
    annual_fee = 120
    cycle_day = 1
    earning_rates = '1.5 point per dollar'
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    # account = models.ForeignKey('Account', on_delete=models.PROTECT)