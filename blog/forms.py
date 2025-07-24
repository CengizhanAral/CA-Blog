from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Comment, Author, Subscriber
from django.utils.translation import gettext_lazy as _

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user and self.user.is_authenticated:
            if 'name' in self.fields:
                del self.fields['name']
            if 'email' in self.fields:
                del self.fields['email']

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('İsminiz')}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('E-posta adresiniz')}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': _('Yorumunuz...')}),
        }
        labels = {
            'name': _('İsim'),
            'email': _('E-posta'),
            'body': _('Yorum'),
        }


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['bio', 'instagram_url', 'twitter_url', 'facebook_url', 'linkedin_url']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': _('E-posta adresinizi girin...')
            })
        }