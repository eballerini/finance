from .models import Transaction

class TransactionRepository:
    
    def create_bulk(self, transactions_data):
        transactions = [Transaction(**transaction) for transaction in transactions_data]
        Transaction.objects.bulk_create(transactions)
        print("transactions saved")
