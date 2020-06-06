from datetime import date

from django.test import TestCase

from .factories import AccountFactory, CreditCardFactory, UserFactory
from .models import Transaction, TransactionImport
from .services import TransactionImportService


class TransactionImportServiceIntegrationTest(TestCase):
    
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.account = AccountFactory(owner=self.user)
        self.credit_card = CreditCardFactory(owner=self.user, account=self.account)
        self.transactions_data = [
            {
                'description': 'Air Canada 123',
                'amount': 345.45,
                'date_added': date(2019, 12, 12),
                'payment_method_type': 'CC',
                'credit_card_id': self.credit_card.id,
                'account_id': self.account.id,
            }
        ]
        self.sut = TransactionImportService()
    
    def test_import_transactions__success(self):
        self.sut.import_transactions(transactions_data=self.transactions_data, filename='sample.txt', credit_card_id=self.credit_card.id)
        
        transactions = Transaction.objects.filter(account_id=self.account.id)
        self.assertEqual(1, len(transactions))
        self.assertIsNotNone(transactions[0].transaction_import_id)
        
        imports = TransactionImport.objects.filter(credit_card_id=self.credit_card.id)
        self.assertEqual(1, len(imports))
        
    def test_import_transactions__failure(self):
        self.fail('TODO')
