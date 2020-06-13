from datetime import date, datetime
from decimal import Decimal
from factory.django import DjangoModelFactory

from . import models


class UserFactory(DjangoModelFactory):
    class Meta:
        model = models.User

    first_name = "John"
    last_name = "Doe"


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = models.Account

    name = "Main"
    currency_code = "CAD"


class CreditCardFactory(DjangoModelFactory):
    class Meta:
        model = models.CreditCard

    name = "Visa"
    # application_date = models.DateField(null=True, blank=True)
    # deadline_minimum_spending = models.DateField(null=True, blank=True)
    # approval_date = models.DateField(null=True, blank=True)
    # cancellation_date = models.DateField(null=True, blank=True)
    minimum_spending = 1000
    signup_bonus = 25000
    first_year_fee = 0
    annual_fee = 120
    cycle_day = 1
    earning_rates = "1.5 point per dollar"


class TransactionFactory(DjangoModelFactory):
    class Meta:
        model = models.Transaction

    description = "Food"
    amount = Decimal("10")
    date_added = date.today()
    payment_method_type = "CC"
    # credit_card = models.ForeignKey('CreditCard', on_delete=models.PROTECT, null=True, blank=True)
    # category = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, blank=True)
    # account = models.ForeignKey('Account', on_delete=models.PROTECT)


class TransactionImportFactory(DjangoModelFactory):
    class Meta:
        model = models.TransactionImport

    created = datetime.now()
    filename = "sample.txt"
    # credit_card = models.ForeignKey('CreditCard', on_delete=models.PROTECT)
