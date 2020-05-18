from django.urls import path

from . import views
from rest_framework_simplejwt import views as jwt_views

from .views import current_user, UserList, UserCreate, HelloWorldView, LogoutAndBlacklistRefreshTokenForUserView, ObtainTokenPairWithColorView, AccountsView, TransactionsView, CreditCardsForFirstAccountView, CategoryView, CreditCardsForAccountView, CreditCardsView

urlpatterns = [
    path('', views.index, name='index'),
    path('user/create/', UserCreate.as_view(), name="create_user"),
    path('token/obtain/', ObtainTokenPairWithColorView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloWorldView.as_view(), name='hello_world'),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    
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
    path('api/accounts/', AccountsView.as_view(), name='account_list'),
    path('api/accounts/<int:account_id>/creditcards/', CreditCardsForAccountView.as_view(), name='credit_card_for_account_list'),
    path('api/transactions/', TransactionsView.as_view(), name='transaction_list'),
    path('api/transactions/<int:transaction_id>/', TransactionsView.as_view(), name='transaction_edit'),
    # TODO remove creditcardsforfirstaccount. Use api/accounts/<int:account_id>/creditcards/ instead
    path('api/creditcardsforfirstaccount/', CreditCardsForFirstAccountView.as_view(), name='credit_card_for_first_account_list'),
    path('api/creditcards/', CreditCardsView.as_view(), name='credit_card_list'),
    path('api/creditcards/<int:credit_card_id>/', CreditCardsView.as_view(), name='credit_card_edit'),
    path('api/categories/', CategoryView.as_view(), name='category_list'),
]
