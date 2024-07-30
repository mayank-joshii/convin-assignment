from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone 
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=15)
       

class Expenses(models.Model):

   name = models.CharField(max_length=50)
   description = models.TextField()
   created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
   total_amount = models.IntegerField()
   split_method = models.CharField(max_length=10, choices=[('equal', 'Equal'), ('exact', 'Exact'), ('percentage', 'Percentage')])

   def save(self, *args, **kwargs):
        if not self.url:
            self.url = get_random_string(50)
        super().save(*args, **kwargs)

class expenseShare(models.Model):
   
   expense = models.ForeignKey(Expenses, related_name='shares', on_delete=models.CASCADE)
   user = models.ForeignKey(User, related_name='shares', on_delete=models.CASCADE)
   amount = models.DecimalField(max_digits=10, decimal_places=2)

   