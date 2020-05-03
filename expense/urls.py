from django.urls import path

from . import views
from rest_framework_simplejwt import views as jwt_views

from .views import current_user, UserList, UserCreate, HelloWorldView, LogoutAndBlacklistRefreshTokenForUserView

urlpatterns = [
    path('', views.index, name='index'),
    path('user/create/', UserCreate.as_view(), name="create_user"),
    path('token/obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
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
    path('api/accounts/', views.accounts_as_json, name='accounts_as_json'),
    path('api/categories/', views.categories_as_json, name='categories_as_json'),
    path('api/transactions/', views.transactions_for_first_account_as_json, name='transactions_for_first_account_as_json'),
    path('api/creditcards/', views.credit_cards_for_first_account, name='credit_cards_for_first_account'),
    
]
