from django import forms 
from auctions.models import List 

CATEGORIES = [ ('test', 'Test') ]

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'starting_price', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'starting_price': forms.NumberInput(attrs = {'class': 'form-control'}),
            'category': forms.Select(choices = CATEGORIES, attrs = {'class': 'form-control'})   
        }
            