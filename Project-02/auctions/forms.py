from django import forms 
from auctions.models import List, Bid, CATEGORIES

class ListForm(forms.ModelForm):
    class Meta:
        model = List
        fields = ['title', 'description', 'img_url', 'starting_price', 'category']
        widgets = {
            'title'             : forms.TextInput(attrs={'class': 'form-control'}),
            'description'       : forms.Textarea(attrs={'class': 'form-control'}),
            'img_url'           : forms.TextInput(attrs = {'class': 'form-control'}),
            'starting_price'    : forms.NumberInput(attrs = {'class': 'form-control'}),
            'category'          : forms.Select(choices = CATEGORIES, attrs = {'class': 'form-control'})   
        }
        
class BidForm(forms.ModelForm):
    class Meta:
        model = Bid 
        fields = ['price']
        widgets = {
            'price'             : forms.TextInput(attrs={'class': 'form-control'})
        }
            