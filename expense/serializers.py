from rest_framework import serializers

from .models import Expense

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'description', 'amount', 'date_added', 'payment_method_type', 'credit_card', 'category', 'account']
