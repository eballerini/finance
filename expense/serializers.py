from rest_framework import serializers
#from rest_framework_jwt.settings import api_settings
#from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


from .models import Account, Category, CreditCard, Transaction, User

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'name', 'currency_code']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class CreditCardSerializerLight(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'name']

# TODO merge these 2 serializers
class CreditCardSerializer(serializers.ModelSerializer):
    account = AccountSerializer()
    
    class Meta:
        model = CreditCard
        fields = ['id', 'name', 'application_date', 'deadline_minimum_spending', 'approval_date', 'cancellation_date', 'minimum_spending', 'signup_bonus', 'first_year_fee', 'annual_fee', 'cycle_day', 'earning_rates', 'account']
        
class CreditCardSerializerPost(serializers.ModelSerializer):    
    class Meta:
        model = CreditCard
        fields = ['id', 'name', 'application_date', 'deadline_minimum_spending', 'approval_date', 'cancellation_date', 'minimum_spending', 'signup_bonus', 'first_year_fee', 'annual_fee', 'cycle_day', 'earning_rates', 'account']
        
class DashboardSerializer(serializers.Serializer):
    num_credit_cards_opened = serializers.IntegerField()
    first_year_fees = serializers.IntegerField()

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'description', 'amount', 'date_added', 'payment_method_type', 'credit_card', 'category']

# this is a different serializer for the GET request because of the related objects that mess up with the POST requests
class TransactionSerializerGet(TransactionSerializer):
    category = CategorySerializer(required=False)
    credit_card = CreditCardSerializerLight(required=False)


class UserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(
        required=True
    )
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)  # as long as the fields are the same, we can just use this
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token
