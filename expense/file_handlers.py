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

    def serialize_data(self, data, account_id):
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            print("data is valid")
            transaction_data = serializer.validated_data
            transaction_data["account_id"] = account_id
            return transaction_data
        else:
            print("data is invalid")
            print(serializer.errors)
            raise TransactionImportValidationException(serializer.errors)

        return transactions

    def create_data(self, description, amount, formatted_date, credit_card_id):
        data = {
            "description": description,
            "amount": amount,
            "date_added": formatted_date,
            "payment_method_type": "CC",
            "credit_card": credit_card_id,
        }
        return data


class VisaTDCsvFileHandler(BaseCsvFileHandler):
    def parse_transactions(self, credit_card_id, file, credit_card):
        print("credit_card_id: " + credit_card_id)
        print("filename: " + file.name)

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

            data = self.create_data(parts[1], amount, formatted_date, credit_card_id)
            transaction_data = self.serialize_data(data, credit_card.account_id)
            transactions.append(transaction_data)

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
            data = self.create_data(parts[1], parts[2], formatted_date, credit_card_id)
            transaction_data = self.serialize_data(data, credit_card.account_id)
            transactions.append(transaction_data)

        return transactions


class AmexBPCsvFileHandler(BaseCsvFileHandler):
    def parse_transactions(self, credit_card_id, file, credit_card):
        transactions = []
        for line_as_byte in file:
            line = str(line_as_byte, "utf-8")
            print("processing: " + line)
            parts = line.split(" ")
            num_parts = len(parts)
            unformatted_date = f"{parts[0]} {parts[1]} {parts[2]}"
            amount_with_dollar_sign = parts[num_parts - 1]
            amount = amount_with_dollar_sign[1:]  # exclude the $ sign
            description = " ".join(parts[3 : num_parts - 1])
            formatted_date = self.format_date(unformatted_date, "%d %b %Y")

            data = self.create_data(description, amount, formatted_date, credit_card_id)
            transaction_data = self.serialize_data(data, credit_card.account_id)
            transactions.append(transaction_data)

        return transactions
