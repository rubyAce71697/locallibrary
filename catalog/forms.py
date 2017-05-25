from django import forms
from django.contrib.auth.forms import User
from django.core.exceptions import ValidationError
import datetime
from django.utils.translation import ugettext_lazy as _

class UserLoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="Password")
    class Meta:
        model = User
        fields = ('username','password')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks (default 3).')


    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']


        if data < datetime.date.today():
            raise ValidationError(_('Invalid date. Date should be in future'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        return data
def validate_file_extention(value):
        if not value.name.endswith('.csv'):
            raise forms.ValidationError("Only CSV file is accepted")

class AuthorUpLoadForm(forms.Form):
    file = forms.FileField(label = "Authors CSV", validators =[validate_file_extention])


class LanguageUpLoadForm(forms.Form):
    file = forms.FileField(label = "Languages CSV", validators =[validate_file_extention])

class GenereUpLoadForm(forms.Form):
    file = forms.FileField(label = "Genere CSV", validators =[validate_file_extention])



