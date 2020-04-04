from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Account, Category
from .forms import CategoryForm

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
    