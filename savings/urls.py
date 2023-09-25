from django.urls import path
from . import views


urlpatterns = [
   path('contribute/', views.savings, name="contribute"),
   path('balance/', views.checkBalance, name="balance"),
   path('total/', views.viewTotal, name="total"),

   
   path('withdraw/', views.withdrawCash, name="withdraw"),
   path('view_contributions/', views.viewContribution, name="view_contributions"),
   path('contributions_histroy/', views.contributionHistory, name="contributions_histroy"),
   path('download_contributions/', views.downloadContributions, name="download_contributions"),

   path('view_users/', views.viewUsers, name="view_users"),
   path('all_users/', views.allUsers, name="all_users"),
   path('activate_user/<str:pk>/', views.activateUsers, name="activate_user"),
   path('deactivate_user/<str:pk>/', views.deactivateUsers, name="deactivate_user"),
   path('verify_contributions/<str:pk>/', views.verifyContribution, name="verify_contributions"),
   path('decline_contributions/<str:pk>/', views.declineContribution, name="decline_contributions"),
   path('sendmoney/<str:pk>/', views.sendMoney, name="sendmoney"),



 
 

]
