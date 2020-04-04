from django import forms

class CategoryForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)