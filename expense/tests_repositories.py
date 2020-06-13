from django.test import TestCase

from .factories import (
    AccountFactory,
    CreditCardFactory,
    UserFactory,
    TransactionFactory,
    TransactionImportFactory,
)
from .models import Transaction, TransactionImport
from datetime import date
from .repositories import TransactionRepository


class TransactionRepositoryTests(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.another_user = UserFactory(username="wi")
        self.account = AccountFactory(owner=self.user)
        self.another_account = AccountFactory(owner=self.another_user)
        self.credit_card = CreditCardFactory(owner=self.user, account=self.account)
        self.import1 = TransactionImportFactory(credit_card_id=self.credit_card.id)
        self.transaction1 = TransactionFactory(
            date_added=date(2019, 12, 12),
            account_id=self.account.id,
            transaction_import_id=self.import1.id,
        )
        self.transaction2 = TransactionFactory(
            date_added=date(2018, 11, 12),
            account_id=self.account.id,
            transaction_import_id=self.import1.id,
        )
        self.transaction3 = TransactionFactory(
            date_added=date(2020, 1, 2), account_id=self.account.id
        )
        self.transaction4 = TransactionFactory(
            date_added=date(2020, 1, 2), account_id=self.another_account.id
        )
        self.sut = TransactionRepository()

    def test_list__success(self):
        filters = {
            "account_id": self.account.id,
        }
        result = self.sut.list(filters)
        self.assertEqual(3, len(result))
        self.assertEqual(self.transaction2, result[0])
        self.assertEqual(self.transaction1, result[1])
        self.assertEqual(self.transaction3, result[2])

    def test_list_by_import_id__success(self):
        filters = {
            "account_id": self.account.id,
            "transaction_import_id": self.import1.id,
        }
        result = self.sut.list(filters)
        self.assertEqual(2, len(result))
        self.assertEqual(self.transaction2, result[0])
        self.assertEqual(self.transaction1, result[1])
