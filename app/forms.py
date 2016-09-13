# -*- coding: utf-8 -*-
from django import forms


class SurveyForm(forms.Form):
    def __init__(self, prices, based, platforms,
                 dynamic, extra, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['Price'].choices = prices
        self.fields['Based'].choices = based
        self.fields['Platform'].choices = platforms
        self.fields['Dynamic'].choices = dynamic
        self.fields['Extra'].choices = extra

    Price = forms.ChoiceField(choices=(), required=True, label='Preço')
    Based = forms.ChoiceField(choices=(), required=True, label="Baseado")
    Platform = forms.ChoiceField(choices=(), required=True, label="Plataforma")
    Dynamic = forms.ChoiceField(choices=(), required=True, label="Dinamica")
    Extra = forms.ChoiceField(choices=(), required=True)


class UserFormLogin(forms.Form):
    UserName = forms.CharField(required=True, max_length=100, label="Username")
    Password = forms.CharField(required=True, max_length=32, widget=forms.PasswordInput, label="Password")


class UserFormSignUp(forms.Form):
    UserName = forms.CharField(required=True, max_length=100, label="Username")
    Email = forms.CharField(required=True, max_length=100, label="Email")
    FirstName = forms.CharField(required=True, max_length=200, label="First Name")
    LastName = forms.CharField(required=True, max_length=200, label="Last Name")
    Password = forms.CharField(required=True, max_length=32, widget=forms.PasswordInput, label="Password")
    Confirm = forms.CharField(required=True, max_length=32, widget=forms.PasswordInput, label="Confirm Password")


class UpdatePasswordForm(forms.Form):
    NewPasswd = forms.CharField(required=True, max_length=32, widget=forms.PasswordInput, label="New Password")
    Confirm = forms.CharField(required=True, max_length=32, widget=forms.PasswordInput, label="Confirm Password")


class IndicateCourseForm(forms.Form):
    def __init__(self, types, courses, *args, **kwargs):
        super(IndicateCourseForm, self).__init__(*args, **kwargs)
        self.fields['Type'].choices = types
        self.fields['Course'].choices = courses
    Type = forms.ChoiceField(choices=(), required=True)
    Course = forms.ChoiceField(choices=(), required=True)
    Name = forms.CharField(max_length=355, required=True, label="Nome do curso")
    Url = forms.CharField(max_length=355, required=True, label="Endereco do curso")
