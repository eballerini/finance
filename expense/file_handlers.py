from itertools import islice
from datetime import datetime

from .serializers import TransactionSerializer


class BaseCsvFileHandler:
    def parse_transactions(self, credit_card_id, file, credit_card):
        pass


class VisaTDCsvFileHandler:
    def parse_transactions(self, credit_card_id, file, credit_card):
        print("credit_card_id: " + credit_card_id)
        print("filename: " + file.name)
        # TODO move this to repo
        transactions = []
        errors = None
        for line_as_byte in file:
            line = str(line_as_byte, "utf-8")
            print("processing: " + line)
            parts = line.split(",")
            if parts[2] != "":
                amount = parts[2]
            elif parts[3] != "":
                amount = "-" + parts[3]
            else:
                errors = {"amount": "cannot parse amount"}
                break

            try:
                formatted_date = datetime.strptime(parts[0], "%m/%d/%Y").strftime(
                    "%Y-%m-%d"
                )
            except ValueError as e:
                print(e)
                errors = {"date": str(e)}
                break

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
                errors = serializer.errors
                break

        return transactions, errors


class AmexUSHiltonCsvFileHandler:
    def parse_transactions(self, credit_card_id, file, credit_card):
        transactions = []
        errors = None
        first_line = str(file.readline().rstrip(), "utf-8")
        print(f"first line: {first_line}")
        if first_line != "Date,Description,Amount":
            errors = {"header": "header is different than what's expected"}
            return {}, errors

        # rewind to the beginning of the file
        file.seek(0)

        for line_as_byte in islice(file, 1, None):
            line = str(line_as_byte, "utf-8")
            print(line)
            parts = line.split(",")

            try:
                formatted_date = datetime.strptime(parts[0], "%m/%d/%y").strftime(
                    "%Y-%m-%d"
                )
            except ValueError as e:
                print(e)
                errors = {"date": str(e)}
                break

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
                errors = serializer.errors
                break
        # Date,Description,Amount
        # 5/24/20,VIMEO,95.80

        return transactions, errors
