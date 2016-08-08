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

