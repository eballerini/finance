from django.contrib import admin

# Register your models here.
from .models import Account, CreditCard, Category, Expense

admin.site.register(Account)
admin.site.register(CreditCard)
admin.site.register(Category)
admin.site.register(Expense)