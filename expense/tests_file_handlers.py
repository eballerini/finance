from collections import OrderedDict
from decimal import Decimal
from datetime import date
from django.test import TestCase
from .file_handlers import VisaTDCsvFileHandler
from .factories import (
    AccountFactory,
    CreditCardFactory,
    UserFactory,
    TransactionFactory,
    TransactionImportFactory,
)


class VisaTDCsvFileHandlerTests(TestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory()
        self.another_user = UserFactory(username="wi")
        self.account = AccountFactory(owner=self.user)
        self.another_account = AccountFactory(owner=self.another_user)
        self.credit_card = CreditCardFactory(owner=self.user, account=self.account)
        self.sut = VisaTDCsvFileHandler()

    def test__success(self):
        file = open("expense/test-files/TD/accountactivity-1credit-1debit.csv", "rb")
        transactions, errors = self.sut.parse_transactions(
            str(self.credit_card.id), file, self.credit_card
        )
        self.assertIsNone(errors)
        self.assertEqual(2, len(transactions))
        expected_transaction = {
            "description": "PAYMENT",
            "amount": Decimal("-2000.00"),
            "date_added": date(2019, 10, 11),
            "payment_method_type": "CC",
            "credit_card": self.credit_card,
            "account_id": self.credit_card.account_id,
        }
        self.assertEqual(OrderedDict(expected_transaction), transactions[0])
        expected_transaction = {
            "description": "ROWE FARM",
            "amount": Decimal("9.03"),
            "date_added": date(2019, 11, 4),
            "payment_method_type": "CC",
            "credit_card": self.credit_card,
            "account_id": self.credit_card.account_id,
        }
        self.assertEqual(OrderedDict(expected_transaction), transactions[1])
