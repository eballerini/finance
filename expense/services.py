from .repositories import TransactionRepository, TransactionImportRepository

class TransactionImportService:
    
    def __init__(self):
        self.transaction_repository = TransactionRepository()
        self.transaction_import_repository = TransactionImportRepository()
    
    def import_transactions(self, transactions_data, filename, credit_card_id):        
        import_transaction_data = {
            'filename': filename, 
            'credit_card_id' : credit_card_id,
        }
        # TODO add tx
        transaction_import = self.transaction_import_repository.create(import_transaction_data)
        for transaction_data in transactions_data:
            transaction_data['transaction_import_id'] = transaction_import.id
            
        self.transaction_repository.create_bulk(transactions_data)
