from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django import forms

from accounts.models import Profile


class MyUserCreationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        strip=False,
        required=True,
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='Repeat password',
        strip=False,
        required=True,
    )
    email = forms.EmailField(required=True, label='Email', widget=forms.EmailInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('The passwords are not the same')
        if not first_name and not last_name:
            raise forms.ValidationError('At least first name or last name must be provided')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_confirm',
            'first_name',
            'last_name',
            'email',
        ]


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']


class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(strip=False, label='Password', widget=forms.PasswordInput)
    password_confirm = forms.CharField(strip=False, label='Password confirm', widget=forms.PasswordInput)
    old_password = forms.CharField(strip=False, label='Old password', widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords confirmation error')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Incorrect old password')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ['password', 'password_confirm', 'old_password']
