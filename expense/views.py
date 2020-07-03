from .file_handlers import (
    VisaTDCsvFileHandler,
    AmexUSHiltonCsvFileHandler,
    AmexBPCsvFileHandler,
)
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.views import generic
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .exceptions import TransactionImportValidationException
from .forms import CategoryForm, CreditCardForm, UploadFileForm
from .models import Account, Category, CreditCard, Transaction
from .serializers import (
    AccountSerializer,
    CategorySerializer,
    CreditCardSerializer,
    CreditCardSerializerLight,
    CreditCardSerializerPost,
    DashboardSerializer,
    MyTokenObtainPairSerializer,
    TransactionSerializer,
    TransactionSerializerGet,
    UserSerializer,
)
from .services import TransactionImportService
from .repositories import TransactionRepository


class HelloWorldView(APIView):
    def get(self, request):
        return Response(data={"hello": "world"}, status=status.HTTP_200_OK)


class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ObtainTokenPairWithColorView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


@login_required
def index(request):
    return render(request, template_name="expense/index.html")


@login_required
def accounts(request):
    # TODO move to repo layer
    accounts = Account.objects.filter(owner=request.user)

    template = loader.get_template("expense/accounts.html")
    context = {
        "account_list": accounts,
    }
    return HttpResponse(template.render(context, request))


@login_required
def categories(request):
    categories = Category.objects.filter(owner=request.user)
    template = loader.get_template("expense/categories.html")
    context = {
        "category_list": categories,
    }
    return HttpResponse(template.render(context, request))


@login_required
def add_category(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Category.objects.create(name=form.cleaned_data["name"], owner=request.user)

            return redirect("/expense/categories")
    else:
        form = CategoryForm()

    return render(request, "expense/category_detail.html", {"form": form})


@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # TODO move to repo
            category.name = form.cleaned_data["name"]
            category.save()

            return redirect("/expense/categories")
    else:
        form = CategoryForm(initial={"name": category.name})

    return render(request, "expense/category_detail.html", {"form": form})


class CreditCardListView(generic.ListView):
    template_name = "expense/credit_cards.html"
    context_object_name = "credit_card_list"

    def get_queryset(self):
        return CreditCard.objects.filter(owner=self.request.user)


@login_required
def add_credit_card(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = CreditCardForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            CreditCard.objects.create(
                name=form.cleaned_data["name"],
                application_date=form.cleaned_data["application_date"],
                deadline_minimum_spending=form.cleaned_data[
                    "deadline_minimum_spending"
                ],
                approval_date=form.cleaned_data["approval_date"],
                cancellation_date=form.cleaned_data["cancellation_date"],
                minimum_spending=form.cleaned_data["minimum_spending"],
                signup_bonus=form.cleaned_data["signup_bonus"],
                first_year_fee=form.cleaned_data["first_year_fee"],
                annual_fee=form.cleaned_data["annual_fee"],
                cycle_day=form.cleaned_data["cycle_day"],
                earning_rates=form.cleaned_data["earning_rates"],
                owner=request.user,
            )

            return redirect("/expense/creditcards")
    else:
        form = CreditCardForm()

    return render(request, "expense/credit_card_detail.html", {"form": form})


class AccountsView(APIView):
    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)
        serializer = AccountSerializer(accounts, many=True)

        return JsonResponse(serializer.data, safe=False)


class TransactionsView(APIView):
    def get(self, request, account_id):
        print("getting transactions for account " + str(account_id))

        transaction_repository = TransactionRepository()
        filters = {
            "account_id": account_id,
        }
        if request.GET.get("transaction_import_id"):
            filters["transaction_import_id"] = request.GET.get("transaction_import_id")

        transactions = transaction_repository.list(filters)
        serializer = TransactionSerializerGet(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request, account_id):
        print("creating transaction...")
        account = _get_account(request.user, account_id)

        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(account=account)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, account_id, transaction_id):
        print("updating transaction...")
        account = _get_account(request.user, account_id)

        # TODO move this to repo
        transaction = Transaction.objects.get(id=transaction_id, account=account)

        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(account=account)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, account_id, transaction_id):
        print("deleting transaction...")
        account = _get_account(request.user, account_id)
        # TODO move this to repo
        transaction = Transaction.objects.get(id=transaction_id, account=account)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreditCardsForAccountView(APIView):
    def get(self, request, account_id):
        credit_cards = CreditCard.objects.filter(
            account_id=account_id, owner=request.user
        )
        serializer = CreditCardSerializerLight(credit_cards, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


class DashboardView(APIView):
    def get(self, request):
        today = date.today()
        one_year_ago = today - timedelta(days=365)
        credit_cards = CreditCard.objects.filter(
            owner=request.user, application_date__gte=one_year_ago
        ).order_by("approval_date")
        num_credit_cards_opened = credit_cards.count()
        credit_card_fees = [credit_card.first_year_fee for credit_card in credit_cards]
        first_year_fees = sum(credit_card_fees)

        if num_credit_cards_opened > 0:
            last_approval_date = credit_cards.last().approval_date
        else:
            last_approval_date = None

        serializer = DashboardSerializer(
            data={
                "num_credit_cards_opened": num_credit_cards_opened,
                "first_year_fees": first_year_fees,
                "last_approval_date": last_approval_date,
            }
        )
        if serializer.is_valid():
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreditCardsView(APIView):
    def get(self, request):
        print("loading credit cards...")
        sort = request.GET.get("sort")
        order_by = "name" if sort == "name" else "application_date"
        credit_cards = CreditCard.objects.filter(owner=request.user).order_by(order_by)
        serializer = CreditCardSerializer(credit_cards, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    def post(self, request):
        print("creating credit card...")

        serializer = CreditCardSerializerPost(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, credit_card_id):
        print("updating credit card...")
        print(request.data)

        # TODO move this to repo
        credit_card = CreditCard.objects.get(id=credit_card_id, owner=request.user)

        serializer = CreditCardSerializerPost(credit_card, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, credit_card_id):
        print("deleting credit card...")
        credit_card = CreditCard.objects.get(id=credit_card_id, owner=request.user)
        credit_card.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.filter(owner=request.user).order_by("name")
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        print("creating category...")

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, category_id):
        print("updating category...")
        print(request.data)

        # TODO move this to repo
        category = Category.objects.get(id=category_id, owner=request.user)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        print("deleting category...")
        category = Category.objects.get(id=category_id, owner=request.user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TODO remove
def handle_uploaded_file(credit_card_id, file, credit_card):
    print("credit_card_id: " + credit_card_id)
    print("filename: " + file.name)
    # TODO move this to repo
    transactions = []
    errors = None
    for line_as_byte in file:
        line = str(line_as_byte, "utf-8")
        print("processing: " + line)
        parts = line.split(",")
        # print("parts")
        # for part in parts:
        #     print(part)
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

    if errors:
        return {}, errors

    transaction_import_id = -1
    if len(transactions) > 0:
        print(f"saving {len(transactions)} transactions")
        service = TransactionImportService()
        transaction_import_id = service.import_transactions(
            transactions_data=transactions,
            filename=file.name,
            credit_card_id=credit_card_id,
        )
    else:
        print("no transactios to save")

    return {"transaction_import_id": transaction_import_id}, errors


class TransactionsUploadView(APIView):
    def _is_credit_card_of_type(self, keywords, credit_card_name):
        matches = [keyword in credit_card_name for keyword in keywords]
        return all(matches)

    def post(self, request):
        print(request.FILES)
        print(request.data)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            credit_card_id = request.data.get("credit_card_id")
            credit_card = CreditCard.objects.get(id=credit_card_id, owner=request.user)
            credit_card_name = credit_card.name.lower()
            file_handler = None
            if self._is_credit_card_of_type(["td", "visa"], credit_card_name):
                file_handler = VisaTDCsvFileHandler()
            elif self._is_credit_card_of_type(
                ["amex", "us", "hilton"], credit_card_name
            ):
                file_handler = AmexUSHiltonCsvFileHandler()
            elif self._is_credit_card_of_type(
                ["amex", "business", "platinum"], credit_card_name
            ):
                file_handler = AmexBPCsvFileHandler()
            else:
                errors = {"reason": "credit card type not supported"}

            if file_handler:
                file = request.FILES["file"]
                errors = None
                try:
                    transactions = file_handler.parse_transactions(
                        credit_card_id, file, credit_card
                    )
                except TransactionImportValidationException as e:
                    errors = e.errors

            if errors:
                return Response(errors, status=status.HTTP_400_BAD_REQUEST)

            transaction_import_id = -1
            if len(transactions) > 0:
                print(f"saving {len(transactions)} transactions")
                service = TransactionImportService()
                transaction_import_id = service.import_transactions(
                    transactions_data=transactions,
                    filename=file.name,
                    credit_card_id=credit_card_id,
                )
            else:
                print("no transactios to save")

            data = {"transaction_import_id": transaction_import_id}

            return JsonResponse(data, status=status.HTTP_201_CREATED)


def _get_account(user, account_id):
    account = Account.objects.get(owner=user, id=account_id)
    return account


@login_required
def transactions(request, account_id):
    # TODO add owner
    transactions = Transaction.objects.filter(account_id=account_id).select_related(
        "category"
    )
    serializer = TransactionSerializer(transactions, many=True)

    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """

    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
