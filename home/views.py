from django.shortcuts import render, HttpResponse
from home.serializers import UserSerializer, ExpenseShareSerializer, ExpenseSerializer
from rest_framework import generics, permissions
from home.models import  UserProfile, expenseShare, Expenses
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.contrib.auth import get_user_model
import csv
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
# Create your views here.


class RegisterUserview(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer

class ExpenseCreateView(generics.ListCreateAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by = self.request.user)
    

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expenses.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

class ExpenseShareView(generics.ListCreateAPIView):

    queryset = expenseShare.objects.all()
    serializer_class = ExpenseShareSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        expense = serializer.validated_data['expense']

        total_amount = expense.total_amount

        share_amount = serializer.validated_data['amount']

        if share_amount>total_amount:
            raise serializer.ValidationError("Invalid share amount!!!!")
        serializer.save()    

# @api_view(['POST'])
# def split_expense(request, expense_id, method):
#     print(request.data)
#     expense = Expenses.objects.get(id=expense_id)
#     total_amount = expense.total_amount
#     shares_data = request.data['shares']

#     if method == 'equal':
#         equal_share = total_amount / len(shares_data)
#         for share_data in shares_data:
#             user = UserProfile.objects.get(id=share_data['user'])
#             expenseShare.objects.create(expense=expense, user=user, amount=equal_share)

#     elif method == 'exact':
#         for share_data in shares_data:
#             user = UserProfile.objects.get(id=share_data['user'])
#             amount = share_data['amount']
#             expenseShare.objects.create(expense=expense, user=user, amount=amount)

#     elif method == 'percentage':
#         total_percentage = sum(share_data['percentage'] for share_data in shares_data)
#         if total_percentage != 100:
#             return Response({"error": "Percentages must add up to 100."}, status=400)
#         for share_data in shares_data:
#             user = UserProfile.objects.get(id=share_data['user'])
#             percentage = share_data['percentage']
#             amount = (percentage / 100) * total_amount
#             expenseShare.objects.create(expense=expense, user=user, amount=amount)

#     return Response({"message": "Expense split successfully."})


@api_view(['GET'])
def split_exact(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if expense.split_method != 'exact':
        return Response({"detail": "Expense is not split by exact amounts."}, status=400)
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)


@api_view(['GET'])
def split_equal(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if expense.split_method != 'equal':
        return Response({"detail": "Expense is not split equally."}, status=400)
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)

@api_view(['GET'])
def split_percentage(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if expense.split_method != 'percentage':
        return Response({"detail": "Expense is not split by percentage."}, status=400)
    serializer = ExpenseSerializer(expense)
    return Response(serializer.data)


@api_view(['GET'])

def get_balancesheet(request):
    users = UserProfile.objects.all()
    balances = {}

    for user in users:
        user_expenses = expenseShare.objects.filter(user=user).aggregate(Sum('amount'))['amount__sum'] or 0
        user_contributions = Expenses.objects.filter(created_by=user).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        balances[user.email] = user_expenses - user_contributions
    return Response(balances)


@api_view(['GET'])
def download_balance_sheet(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="balance_sheet.csv"'

    writer = csv.writer(response)
    writer.writerow(['Email', 'Balance'])

    balances = get_balancesheet(request).data
    for email, balance in balances.items():
        writer.writerow([email, balance])

    return 


