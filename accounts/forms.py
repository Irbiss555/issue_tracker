from django.contrib.auth.models import User
from django import forms


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