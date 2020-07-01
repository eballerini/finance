from itertools import islice
from datetime import datetime

from .exceptions import TransactionImportValidationException
from .serializers import TransactionSerializer


class BaseCsvFileHandler:
    def parse_transactions(self, credit_card_id, file, credit_card):
        pass

    def format_date(self, unformatted_date, original_format):
        try:
            formatted_date = datetime.strptime(
                unformatted_date, original_format
            ).strftime("%Y-%m-%d")
        except ValueError as e:
            print(e)
            raise TransactionImportValidationException({"date": str(e)})

        return formatted_date


class VisaTDCsvFileHandler(BaseCsvFileHandler):
    def parse_transactions(self, credit_card_id, file, credit_card):
        print("credit_card_id: " + credit_card_id)
        print("filename: " + file.name)
        # TODO move this to repo
        transactions = []
        for line_as_byte in file:
            line = str(line_as_byte, "utf-8")
            print("processing: " + line)
            parts = line.split(",")
            if parts[2] != "":
                amount = parts[2]
            elif parts[3] != "":
                amount = "-" + parts[3]
            else:
                raise TransactionImportValidationException(
                    {"amount": "cannot parse amount"}
                )

            formatted_date = self.format_date(parts[0], "%m/%d/%Y")

            data = {
                "description": parts[1],
                "amount": amount,
                "date_added": formatted_date,
                "payment_method_type": "CC",
                "credit_card": credit_card_id,
            }
            serializer = TransactionSerializer(data=data)
            if serializer.is_valid():
                print("data is valid")
                transaction_data = serializer.validated_data
                transaction_data["account_id"] = credit_card.account_id
                transactions.append(transaction_data)
            else:
                print("data is invalid")
                print(serializer.errors)
                raise TransactionImportValidationException(serializer.errors)

        return transactions


AMEX_US_HILTON_EXPECTED_HEADER = "Date,Description,Amount"


class AmexUSHiltonCsvFileHandler(BaseCsvFileHandler):
    def parse_transactions(self, credit_card_id, file, credit_card):
        transactions = []
        first_line = str(file.readline().rstrip(), "utf-8")
        print(f"first line: {first_line}")
        if first_line != AMEX_US_HILTON_EXPECTED_HEADER:
            raise TransactionImportValidationException(
                {"header": f"header is not {AMEX_US_HILTON_EXPECTED_HEADER}"}
            )

        # rewind to the beginning of the file
        file.seek(0)

        for line_as_byte in islice(file, 1, None):
            line = str(line_as_byte, "utf-8")
            print(line)
            parts = line.split(",")

            formatted_date = self.format_date(parts[0], "%m/%d/%y")

            data = {
                "description": parts[1],
                "amount": parts[2],
                "date_added": formatted_date,
                "payment_method_type": "CC",
                "credit_card": credit_card_id,
            }
            serializer = TransactionSerializer(data=data)
            if serializer.is_valid():
                print("data is valid")
                transaction_data = serializer.validated_data
                transaction_data["account_id"] = credit_card.account_id
                transactions.append(transaction_data)
            else:
                print("data is invalid")
                print(serializer.errors)
                raise TransactionImportValidationException(serializers.errors)

        return transactions
