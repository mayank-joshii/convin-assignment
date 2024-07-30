from django.contrib import admin
from django.urls import path, include
from home.views import RegisterUserview, ExpenseCreateView, ExpenseDetailView, ExpenseShareView,  get_balancesheet, download_balance_sheet, split_exact, split_equal, split_percentage 

urlpatterns = [
    path('register/', RegisterUserview.as_view(), name='register'),
    path('expenses/', ExpenseCreateView.as_view(), name='expenses-list'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:pk>/split/exact/', split_exact, name='split-expense'),
    path('expenses/<int:pk>/split/equal/', split_equal, name='split-expense'),
    path('expenses/<int:pk>/split/percentage/', split_percentage, name='split-expense'),
    path('shares/', ExpenseShareView.as_view(), name='expense-share'),
    path('balance-sheet/', get_balancesheet, name='balance-sheet'),
    path('balance-sheet/download/', download_balance_sheet, name='download-balance-sheet'),
]