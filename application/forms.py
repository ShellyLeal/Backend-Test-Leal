from django import forms
from .models import menu, lunch


class menuForm(forms.ModelForm):
    '''The form for the menu model'''
    class Meta:
        model = menu
        fields = '__all__'
        exclude = {'uuid'}
        labels = {
            'optionOne': 'Option 1',
            'optionTwo': 'Option 2',
            'optionThree': 'Option 3',
            'optionFour': 'Option 4',  
            'date': 'Date'        
        }
        help_texts = {
            'date': 'Format YYYY-MM-DD',
        }


class lunchForm(forms.ModelForm):
    '''The form for employees to fill their 
    preferred day's meal'''
    class Meta:
        model = lunch
        fields = '__all__'
        exclude = {'user'}
        labels = {
            'user': 'the user',
            'option': 'Choose your preferred meal',
            'preference': 'Any custom preference?',
        }
