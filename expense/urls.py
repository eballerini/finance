from django.urls import path

from . import views

from .views import current_user, UserList

urlpatterns = [
    path('', views.index, name='index'),
    path('current_user/', current_user),
    path('users/', UserList.as_view()),
    path('accounts/', views.accounts, name='accounts'),
    path('accounts/<int:account_id>/transactions', views.transactions, name='transactions'),
    path('categories/', views.categories, name='categories'),
    path('categories/add', views.add_category, name='categories_add'),
    path('categories/<int:category_id>', views.edit_category, name='categories_edit'),
    path('creditcards/', views.CreditCardListView.as_view(), name='credit_cards'),
    path('creditcards/add', views.add_credit_card, name='creditcards_add'),
    
    # TODO move api at the beginning of the URL (in front of expenses)
    path('api/accounts/', views.accounts_as_json, name='accounts_as_json'),
    path('api/categories/', views.categories_as_json, name='categories_as_json'),
    path('api/transactions/', views.transactions_for_first_account_as_json, name='transactions_for_first_account_as_json'),
    path('api/creditcards/', views.credit_cards_for_first_account, name='credit_cards_for_first_account'),
    
]