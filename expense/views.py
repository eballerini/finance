from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .models import Account

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
