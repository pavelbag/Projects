from .models import Post
from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        group = Group.objects.get(name='common')

        user.groups.add(group)
        user.save()

        return user


class PostForm(forms.ModelForm):
    class Meta:
        model = Post

        fields = [
            'post_type',
            'author',
            'title',
            'date',
            'text',
            'categories',
            'rating',
        ]

        labels = {
            'post_type': 'Тип',
            'author': 'Автор',
            'title': 'Заголовок',
            'date': 'Дата',
            'text': 'Текст',
            'categories': 'Категории',
            'rating': 'Рейтинг',
        }

        widgets = {
            'post_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'author': forms.Select(attrs={
                'class': 'form-select'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control'
            }),
            'categories': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Устанавливаем первый вариант в списке
        self.fields['author'].empty_label = ''
        # Устанавливаем нередактируемые поля
        self.fields['post_type'].disabled = True
        self.fields['rating'].disabled = True
        # Инициализируем начальные значения
        self.fields['post_type'].initial = self.Meta.model.post_type