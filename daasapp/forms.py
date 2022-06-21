from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import DAAS_User
from django.contrib.auth import authenticate 

class UserRegister(UserCreationForm):
    phone_number = forms.IntegerField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=200)
    # passwordConf = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = DAAS_User
        fields = ('phone_number', 'first_name', 'last_name',  'email', 'password1', 'password2',)
        def clean_phone_number(self):
            phone_number = self.cleaned_data['phone_number'].lower()
            try:
                user = DAAS_User.objects.get(phone_number=phone_number)
            except Exception as e:
                return phone_number
            raise forms.ValidationError(f'phone number {phone_number} is already in use.')
        def clean_email(self):
            email = self.cleaned_data['email'].lower()
            try:
                user = DAAS_User.objects.get(email=email)
            except Exception as e:
                return email
            raise forms.ValidationError(f'Email {email} is already in use.')
    # def clean(self):
    #     cleaned_data = super().clean()
    #     if self.is_valid():
    #         password = cleaned_data['password']
    #         passwordConf = cleaned_data['passwordConf']
    #         if not authenticate(password = password, passwordConf = passwordConf):
    #             raise forms.ValidationError("Passwords do not match")

    # def clean_passwordConf(self):
    #     password = self.cleaned_data.get('password')
    #     passwordConf = self.cleaned_data.get('passwordConf')
    #     if password != passwordConf:
    #         raise forms.ValidationError("Your passwords do not match")
    #     return passwordConf
        


class UserLogin(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    class Meta:
        model = DAAS_User
        fields = ('email', 'password')
    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate( email = email, password = password):
                raise forms.ValidationError("The email or password you entered is invalid.")