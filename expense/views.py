from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Account

# Create your views here.
def index(request):
    return HttpResponse("Hello. You're at the expense index.")
    
@login_required
def accounts(request):
    accounts = Account.objects.filter(owner=request.user)

    template = loader.get_template('expense/accounts.html')
    context = {
        'account_list': accounts,
    }
    return HttpResponse(template.render(context, request))
