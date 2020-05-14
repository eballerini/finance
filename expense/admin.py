from django.contrib import admin

# Register your models here.
from .models import Account, CreditCard, Category, Transaction, User

admin.site.register(Account)
admin.site.register(CreditCard)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(User)