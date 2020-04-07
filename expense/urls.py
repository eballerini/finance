from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/<int:account_id>/transactions', views.transactions, name='transactions'),
    path('categories/', views.categories, name='categories'),
    path('categories/add', views.add_category, name='categories_add'),
    path('categories/<int:category_id>', views.edit_category, name='categories_edit'),
    path('creditcards/', views.CreditCardListView.as_view(), name='credit_cards'),
    path('creditcards/add', views.add_credit_card, name='creditcards_add'),
]