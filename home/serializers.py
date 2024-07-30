from rest_framework import serializers, generics
from home.models import UserProfile, Expenses, expenseShare, UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email' ]

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'mobile_number']


class ExpenseShareSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = expenseShare
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    shares = ExpenseShareSerializer(many=True, read_only=True)
    class Meta:
        model = Expenses
        fields = ['id', 'name', 'description', 'total_amount', 'created_by', 'shares']
        read_only_field= ['created_by']