from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from . import util
from .forms import WikiEntry

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def wiki(request, title):
    
    """
    Wiki view for showing the wiki page if available.
    Shows error page if wiki page is not available.
    """
    
    entry = util.get_entry(title)
    
    if entry is None: 
        return render(request, "encyclopedia/error.html")
    
    return render(request, "encyclopedia/wiki.html",{
        "title": title.capitalize(),
        "content": entry
    })
    
def search(request):
    
    """
    Search view for searching through wiki entry.
    Displays the wiki entry of the searched entry.
    If searched entry is not found, check if a substring of the searched entry exists 
    in the list of all the entries, and display the list to the user.
    """
    
    searched = request.GET.get('q')
    entry = util.get_entry(searched)
    
    if entry is None:
        substr_entries = []
        entries = util.list_entries()
        for ent in entries:
            if searched in ent.lower():
                substr_entries.append(ent)
            
        if len(substr_entries) == 0:
            return render(request, "encyclopedia/error.html")
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": substr_entries
            })
            
    title = searched.lower()
    
    return render(request, "encyclopedia/wiki.html", {
        "title": title.capitalize(),
        "content": entry    
    })
    
def new_entry(request):
    
    if request.method == "POST":
        form = WikiEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if util.get_entry(title) is None:
                print('entry does not exist')
                util.save_entry(title, content)
                return HttpResponseRedirect(f"wiki/{title}")
            else:
                return render(request, "encyclopedia/new_entry.html", {
                    "form" : form,
                    "success": "false"
                })
                
                
            
    form = WikiEntry()
    return render(request, "encyclopedia/new_entry.html", {
        "form": form
    })

