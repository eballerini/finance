from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template import loader
from django.views import generic
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .forms import CategoryForm, CreditCardForm
from .models import Account, Category, CreditCard, Transaction
from .serializers import AccountSerializer, CategorySerializer, CreditCardSerializer, CreditCardSerializerLight, CreditCardSerializerPost, TransactionSerializer, TransactionSerializerGet, UserSerializer, MyTokenObtainPairSerializer


class HelloWorldView(APIView):

    def get(self, request):
        return Response(data={"hello":"world"}, status=status.HTTP_200_OK)

class UserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    def post(self, request, format='json'):
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
    return render(request, template_name='expense/index.html')
    
@login_required
def accounts(request):
    # TODO move to repo layer
    accounts = Account.objects.filter(owner=request.user)

    template = loader.get_template('expense/accounts.html')
    context = {
        'account_list': accounts,
    }
    return HttpResponse(template.render(context, request))
    
@login_required
def categories(request):
    categories = Category.objects.filter(owner=request.user)
    template = loader.get_template('expense/categories.html')
    context = {
        'category_list': categories,
    }
    return HttpResponse(template.render(context, request))
    
@login_required
def add_category(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Category.objects.create(name=form.cleaned_data["name"], owner=request.user)
            
            return redirect('/expense/categories')
    else:
        form = CategoryForm()
        
    return render(request, 'expense/category_detail.html', {'form': form})
    
@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # TODO move to repo
            category.name = form.cleaned_data["name"]
            category.save()
            
            return redirect('/expense/categories')
    else:
        form = CategoryForm(initial={'name': category.name})
    
    return render(request, 'expense/category_detail.html', {'form': form})
    
class CreditCardListView(generic.ListView):
    template_name = 'expense/credit_cards.html'
    context_object_name = 'credit_card_list'

    def get_queryset(self):
        return CreditCard.objects.filter(owner=self.request.user)
    
@login_required
def add_credit_card(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreditCardForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            CreditCard.objects.create(
                name=form.cleaned_data["name"], 
                application_date=form.cleaned_data["application_date"],
                deadline_minimum_spending=form.cleaned_data["deadline_minimum_spending"],
                approval_date=form.cleaned_data["approval_date"],
                cancellation_date=form.cleaned_data["cancellation_date"],
                minimum_spending=form.cleaned_data["minimum_spending"],
                signup_bonus=form.cleaned_data["signup_bonus"],
                first_year_fee=form.cleaned_data["first_year_fee"],
                annual_fee=form.cleaned_data["annual_fee"],
                cycle_day=form.cleaned_data["cycle_day"],
                earning_rates=form.cleaned_data["earning_rates"],
                owner=request.user
            )
            
            return redirect('/expense/creditcards')
    else:
        form = CreditCardForm()
        
    return render(request, 'expense/credit_card_detail.html', {'form': form})

class AccountsView(APIView):

    def get(self, request):
        accounts = Account.objects.filter(owner=request.user)
        serializer = AccountSerializer(accounts, many=True)
        
        return JsonResponse(serializer.data, safe=False)
        
class TransactionsView(APIView):
    
    def _get_transaction(user, transaction_id):
        first_account = _get_first_account(user)
        try:
            transaction = Transaction.objects.get(id=transaction_id, account=first_account)
        except Transaction.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return transaction
    
    def get(self, request):
        print("getting transactions...")
        first_account = _get_first_account(request.user)
        
        transactions = Transaction.objects.filter(account_id=first_account.id).order_by('date_added')
        serializer = TransactionSerializerGet(transactions, many=True)        
        return JsonResponse(serializer.data, safe=False)
        
    def post(self, request):
        print("creating transaction...")
        first_account = _get_first_account(request.user)
        
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(account=first_account)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, transaction_id):
        print('updating transaction...')
        first_account = _get_first_account(request.user)
        
        # TODO move this to repo
        transaction = Transaction.objects.get(id=transaction_id, account=first_account)
        
        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(account=first_account)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, transaction_id):
        print('deleting transaction...')
        transaction = TransactionsView._get_transaction(request.user, transaction_id)
        transaction.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
# TODO get rid of this in favour of CreditCardsForAccountView
class CreditCardsForFirstAccountView(APIView):
    
    def get(self, request):
        first_account = _get_first_account(request.user)
        credit_cards = CreditCard.objects.filter(account_id=first_account.id)
        serializer = CreditCardSerializerLight(credit_cards, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        
class CreditCardsForAccountView(APIView):
    
    def get(self, request, account_id):
        credit_cards = CreditCard.objects.filter(account_id=account_id, owner=request.user)
        serializer = CreditCardSerializerLight(credit_cards, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        
class CreditCardsView(APIView):
    
    def get(self, request):
        credit_cards = CreditCard.objects.filter(owner=request.user).order_by("application_date")
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
        
class CategoryView(APIView):
    
    def get(self, request):
        first_account = _get_first_account(request.user)        
        categories = Category.objects.filter(owner=request.user)
        serializer = CategorySerializer(categories, many=True)
        return JsonResponse(serializer.data, safe=False)
    
def _get_first_account(user):
    accounts = Account.objects.filter(owner=user)
    # TODO check if there are any accounts
    return accounts[0]
    
@login_required
def transactions(request, account_id):
    # TODO add owner
    transactions = Transaction.objects.filter(account_id=account_id).select_related('category')
    serializer = TransactionSerializer(transactions, many=True)
    
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
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
