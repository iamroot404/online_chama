from django.contrib import admin
from django.utils.html import format_html
from .models import  Savings, Balance, Amount

# Register your models here.
class SavingsAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'savings', 'transaction_id')


class BalanceAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'balance',)



admin.site.register(Savings, SavingsAdmin)

admin.site.register(Balance, BalanceAdmin)
admin.site.register(Amount)
