from django import forms

class CategoryForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    

# TODO replace with ModelForm
class CreditCardForm(forms.Form):
    name = forms.CharField(max_length=50)
    application_date = forms.DateField(required=False)
    deadline_minimum_spending = forms.DateField(required=False)
    approval_date = forms.DateField(required=False)
    cancellation_date = forms.DateField(required=False)
    mininum_spending = forms.IntegerField(required=False)
    signup_bonus = forms.IntegerField(required=False)
    first_year_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    annual_fee = forms.DecimalField(max_digits=10, decimal_places=2)
    cycle_day = forms.IntegerField(required=False)
    earning_rates = forms.CharField(max_length=200, required=False)