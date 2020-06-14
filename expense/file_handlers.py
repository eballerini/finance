from datetime import datetime

from .serializers import TransactionSerializer


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
            if parts[2] == "":
                print("this is not a debit")
                continue

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

        # if errors:
        #     return {}, errors

        return transactions, errors
