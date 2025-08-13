from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    '''Форма отзыва пользователя'''

    class Meta:
        model = Review
        fields = ['text_review', 'rating']
        widgets = {
            'rating': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control'
            }),
            'text_review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),
        }
