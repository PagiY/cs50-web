from django.shortcuts import render

from . import util


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

