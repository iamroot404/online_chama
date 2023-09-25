from datetime import datetime
from email import message
from multiprocessing import context
from re import sub
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import SavingsForm
from . models import  Savings, Balance, Amount
from users.models import Account, UserProfile
from datetime import date
import string    
import random
from django.db.models import Sum
from django.template import loader
from django.http import HttpResponse
import pdfkit

# Create your views here.

@login_required(login_url= 'login')
def savings(request):
    current_user = request.user
    form = SavingsForm()

    if request.method == 'POST':
        form = SavingsForm(request.POST)
        if form.is_valid:
            saving = form.save(commit=False)
            saving.user = current_user

            
            #trans id
            S = 10
            ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")

            transaction_id = current_date + str(ran)
            saving.transaction_id = transaction_id
            saving.balance = 0
            saving.save()
            messages.success(request, 'Your Contribution has been sent please wait for Admin Verification!')
            return redirect('contribute')

    context = {
        'form': form,
    }

    return render(request, 'savings/savings.html', context)

@login_required(login_url= 'login')
def contributionHistory(request):
    current_user = request.user 
    try:
        savings = Savings.objects.filter(user=current_user, is_verified=True).exclude(savings=0)
        
        context = {
        'savings': savings,
        
        }
        return render(request, 'savings/history.html', context)
    except(Balance.DoesNotExist):
        messages.error(request, 'Savings unavailable please contact admin!')
        return redirect('account')

@login_required(login_url= 'login')
def downloadContributions(request):
    current_user = request.user 
    try:
        savings = Savings.objects.filter(user=current_user, is_verified=True).exclude(savings=0)
        
        template = loader.get_template('savings/prcont.html')
        html = template.render({'savings':savings})
        options = {
            'page-size':'letter',
            'encoding':"UTF-8",
        }
        pdf = pdfkit.from_string(html,False,options)
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'attachment'
        filename = 'contributions.pdf'
        return response
    except(Balance.DoesNotExist):
        messages.error(request, 'Savings unavailable please contact admin!')
        return redirect('account')



@login_required(login_url= 'login')
def checkBalance(request):
    current_user = request.user 
    try:
        balance = Balance.objects.get(user=current_user)
        
        context = {
        'balance': balance,
        
        }
        return render(request, 'savings/balance.html', context)
    except(Balance.DoesNotExist):
        messages.error(request, 'Balance unavailable please contact admin!')
        return redirect('account')


@login_required(login_url= 'login')
def withdrawCash(request):
    current_user = request.user 
    balance = Balance.objects.get(user=current_user)

    if request.method == 'POST':
        amount = request.POST['amount']

        t_cost = 200
        bal = balance.balance
        avail_amount = bal - t_cost
        
        if int(amount) >= avail_amount:
            messages.error(request, 'Failed To Withdraw Insufficient Balance ')
        else:
            withdraw = int(amount) + t_cost
            tot = bal - withdraw
            balance.balance = tot
            balance.save()

    context = {
         'balance': balance,
    }
    return render(request, 'savings/withdraw.html', context)     


def viewTotal(request):
    tott = Amount.objects.get(type='TOTAL')
    
    context = {
        'tott': tott,
    }
    return render(request, 'savings/total.html', context)


#only Admin
@login_required(login_url= 'login')
def viewContribution(request):
    user = request.user
    if  user.is_admin == True:

        savings = Savings.objects.filter(is_verified=False)
        
    
        context = {
            'savings': savings,
        }
        return render(request, 'savings/view_contribution.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')


@login_required(login_url= 'login')
def verifyContribution(request, pk):
    user = request.user
    if  user.is_admin == True:


        try:     

            savings = Savings.objects.get(id=pk)
            tot = Amount.objects.get(type='TOTAL')
           
            

            amount = savings.savings
            # bal = balance.balance
            tott = tot.money

            # total = amount + bal
            # balance.balance = total
            # balance.save()

            # balance.paid = savings
            # balance.save()

            totav = amount + tott
            tot.money = totav
            tot.save()

            savings.is_verified = True
            savings.save()


    
            return redirect('view_contributions')
        except(Balance.DoesNotExist, Savings.DoesNotExist):
            return redirect('account')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def declineContribution(request, pk):
    user = request.user
    if  user.is_admin == True:

        savings = Savings.objects.get(id=pk)
        savings.delete()
        return redirect('view_contributions')

    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def viewUsers(request):
    user = request.user
    if  user.is_admin == True:

        users = UserProfile.objects.filter(user__is_admin=False)
        context = {
            'users': users
        }
        return render(request, 'savings/view_users.html', context)
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')

@login_required(login_url= 'login')
def activateUsers(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_active = True
        users.save()
    
        return redirect('view_users')
    
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')



@login_required(login_url= 'login')
def deactivateUsers(request, pk):
    user = request.user
    if  user.is_admin == True:

        users = Account.objects.get(id=pk)

        users.is_active = False
        users.save()
    

        return redirect('view_users')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')
    


@login_required(login_url= 'login')
def sendMoney(request, pk):
    user = request.user
    if  user.is_admin == True:

        try:

            balance = Balance.objects.get(id=pk)
            total = Amount.objects.get(type='TOTAL')

            if request.method == 'POST':
                amount = request.POST['amount']

                avail_amount = total.money

                if int(amount) >= avail_amount:
                    messages.error(request, 'Failed To Send Money Due To Insufficient Balance ')
                else:

                    bal = balance.balance
                    tot = total.money

                    sendM = int(amount) + bal
                    balance.balance = sendM
                    balance.save()
                    


                    current = tot - int(amount)
                    total.money = current
                    total.save()

                    


            

            context = {
                'balance': balance,
                'total': total,
            }

            return render(request, 'savings/sendmoney.html', context)
        except(Balance.DoesNotExist, Amount.DoesNotExist):
            return redirect('account')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')
        

#REPORT
@login_required(login_url= 'login')
def allUsers(request):
    user = request.user
    if  user.is_admin == True:

        try:
            user_details = UserProfile.objects.filter(user__is_admin=False)
            user_count = UserProfile.objects.filter(user__is_admin=False).count()
            template = loader.get_template('savings/users.html')
            html = template.render({'user_details':user_details, 'user_count': user_count})
            options = {
                'page-size':'letter',
                'encoding':"UTF-8",
            }
            pdf = pdfkit.from_string(html,False,options)
            response = HttpResponse(pdf,content_type='application/pdf')
            response['Content-Disposition'] = 'attachment'
            filename = 'users.pdf'
            return response
        except(Balance.DoesNotExist, Amount.DoesNotExist):
            return redirect('account')
    else:
        messages.error(request, "Access Route Denied!")
        return redirect('account')



            









           
