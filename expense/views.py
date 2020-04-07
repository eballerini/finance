from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views import generic

from .models import Account, Category, CreditCard, Expense
from .forms import CategoryForm, CreditCardForm
from .serializers import TransactionSerializer


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
                mininum_spending=form.cleaned_data["mininum_spending"],
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
    




    
    
# TODO add @login_required
def transactions(request, account_id):
    # TODO add owner
    transactions = Expense.objects.filter(account_id=account_id)
    serializer = TransactionSerializer(transactions, many=True)
    
    return JsonResponse(serializer.data, safe=False)