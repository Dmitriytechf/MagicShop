from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import redirect, render
from django_email_verification import send_email

from .forms import ProfileUpdateForm, UserCreateForm, UserUpdateForm
from .models import Profile

User = get_user_model()


def register_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save() # commit=False - при подключении email
            # user_email = form.cleaned_data.get('email')
            # user_username = form.cleaned_data.get('username')
            # user_password = form.cleaned_data.get('password1')
            
            # #Create new user
            # user = User.objects.create_user(
            #     username=user_username, email=user_email, password=user_password
            # )
            # user.is_active = False
            # send_email(user)
            login(request, user)
            return redirect('shop:products')
    else:
        form = UserCreateForm()

    return render(request, 'account/registration/registration.html', {'form': form})


@login_required
def account_view(request):
    return render(request, 'account/profile/profile.html')


@login_required
def update_account(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'account/profile/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('account:profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'account/profile/edit_profile.html', {'form': form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('shop:products')
     
    return redirect('account:profile')
