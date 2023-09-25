from django.forms import ModelForm
from .models import Savings
from django import forms


class SavingsForm(ModelForm):
    class Meta:
        model = Savings
        fields = ['savings']
    
    def __init__(self, *args, **kwargs):
        super(SavingsForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'