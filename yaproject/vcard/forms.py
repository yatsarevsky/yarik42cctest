from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

from yaproject.vcard.models import VCard


class MemberAccountForm(ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={'maxlength': 75}),
        label=('Email address'))
    password = forms.CharField(widget=forms.PasswordInput,
        label='Your Password')
    r_password = forms.CharField(widget=forms.PasswordInput,
        label='Repeat Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'r_password']

    def clean_email(self):
        data = self.cleaned_data['email']

        if User.objects.filter(email__exact=data).exists():
            raise forms.ValidationError("User with this email already exists")

        return data

    def clean_r_password(self):
        data = self.cleaned_data['r_password']

        if self.cleaned_data['password'] != self.cleaned_data['r_password']:
            raise forms.ValidationError("Passwords should match")

        return data

    def save(self, commit=True):
        user = super(MemberAccountForm, self).save(commit=False)
        password = self.cleaned_data['password']
        user.is_active = True
        user.set_password(password)

        if commit:
            user.save()

        return user


class VCardForm(ModelForm):
    class Meta:
        model = VCard
