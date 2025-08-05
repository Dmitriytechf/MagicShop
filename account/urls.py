from django.urls import path, include
from django.shortcuts import render
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView


app_name = 'account'

urlpatterns = [
    # Registration and verification
    path('register/', views.register_user, name='register'),
    path('email-verification-sent/', 
         lambda request:render(request, 'account/registration/email-verification-sent.html'), 
         name='email-verification-sent'),
    
    # Login & Logout
    path('login/', LoginView.as_view(template_name='account/registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # Account
    path('profile/', views.account_view, name='profile'),
    path('profile/update/', views.update_account, name='update_profile'),
    path('profile/change-password/', views.change_password, name='change_password'),
    path('profile/delete/', views.delete_account, name='delete_account'),
]
