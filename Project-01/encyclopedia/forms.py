from django import forms 

class WikiEntry(forms.Form):
    title = forms.CharField(label = "Title", max_length = 64,
                            widget = forms.TextInput(attrs = {'class': 'form-control'}))
    content = forms.CharField(label = "Content", 
                              max_length = 5000,  
                              widget = forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 20em;'}))
    