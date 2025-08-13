from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.forms.widgets import PasswordInput, TextInput

from .models import Profile

User = get_user_model()


class UserCreateForm(UserCreationForm):
    captcha = CaptchaField(
        label="Подтвердите, что Вы настоящий маг",
        help_text="Решите магический пример"
        )
    
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)
        
        self.fields['email'].label = 'Здесь должен быть Ваш email'
        self.fields['email'].required = True
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот email уже используется')
        
        if len(email) > 254:
            raise forms.ValidationError('Email слишком длинный')

        return email

   
    class Meta:
       model = User
       fields = ('username', 'email', 'password1', 'password2', 'captcha')


class UserUpdateForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop('password')
    
    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control-file', 
                'accept': 'image/*'})
        }
    
    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 2*1024*1024:
                raise forms.ValidationError("Файл слишком большой (максимум 2MB)")
            return avatar
        
        return None
    
