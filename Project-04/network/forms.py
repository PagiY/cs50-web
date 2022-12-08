from django import forms 
from network.models import Post 

class PostForm(forms.ModelForm):    
    class Meta:
        model  = Post 
        fields = ['text']
        labels = {
            'text': ""
        }
        widgets = {
            'text' : forms.Textarea(attrs = {'class':'form-control'})
        }
