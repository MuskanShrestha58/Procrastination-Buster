from django import forms
from .models import (
    User,
    UserProfile,
    Task,
    Goal,
    Category,
    TaskMemo,
    GoalMemo,
    TaskCollaboration,
    GoalCollaboration,
    Notification,
)

from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}),
        label='',
        max_length=150,
        required=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        label='',
        required=True,
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='',
        help_text='Your password can’t be too similar to your other personal information. Your password must contain at least 8 characters. Your password can’t be a commonly used password. Your password can’t be entirely numeric.',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password confirmation'}),
        label='',
        help_text='Enter the same password as before, for verification.',
    )

    class Meta:
        model = User
        fields = ("username", "email")

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if not username.isalnum():
            raise ValidationError('Username should be alphanumeric.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists.')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Passwords don\'t match.')

        return password2


class TaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'image_url',
                  'pdf_file', 'priority', 'status', 'categories']
