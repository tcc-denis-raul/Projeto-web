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

    Price = forms.ChoiceField(choices=(), required=True)
    Based = forms.ChoiceField(choices=(), required=True)
    Platform = forms.ChoiceField(choices=(), required=True)
    Dynamic = forms.ChoiceField(choices=(), required=True)
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
