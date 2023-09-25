from email.policy import default
import profile
from unittest.mock import DEFAULT
from django.db import models
from users.models import Account
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


# Create your models here.
class Savings(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    savings = models.IntegerField()
    is_verified = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)


   

    def __str__(self):
        return self.user.email

    class Meta:
        ordering = ['-created_date']

class Balance(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, blank=True, null=True)
    paid = models.ForeignKey(Savings, on_delete=models.SET_NULL, blank=True, null=True)
    balance = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

  



class Amount(models.Model):
    money = models.IntegerField()
    type = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

    



def createSavings(sender, instance, created, **kwargs):
    if created:
        user = instance
        savings = Savings.objects.create( 
            user = user,
            savings = 0,
            is_verified = True,
            transaction_id =  'None',

        )

def createBalance(sender, instance, created, **kwargs):
    if created:
        user = instance
        balance = Balance.objects.create( 
            user = user,
            balance =  0,

        )
    
    
    
post_save.connect(createSavings, sender=Account) 
post_save.connect(createBalance, sender=Account)