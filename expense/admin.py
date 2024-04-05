from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from .models import Account, Category, CreditCard, Transaction, User

class TransactionAdmin(admin.ModelAdmin):
    search_fields = ["description"]


admin.site.register(Account)
admin.site.register(CreditCard)
admin.site.register(Category)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(User, UserAdmin)
