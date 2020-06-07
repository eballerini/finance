from .models import Transaction, TransactionImport


class TransactionRepository:
    
    def create_bulk(self, transactions_data):
        transactions = [Transaction(**transaction) for transaction in transactions_data]
        Transaction.objects.bulk_create(transactions)
        print("transactions saved")

    def list(self):
        # Transaction.objects.filter(account_id=account_id).order_by('date_added')
        pass

class TransactionImportRepository:

    def create(self, import_transaction_data):
        return TransactionImport.objects.create(**import_transaction_data)
