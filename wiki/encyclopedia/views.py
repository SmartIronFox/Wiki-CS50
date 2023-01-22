from django.shortcuts import render
from markdown2 import Markdown 
from . import util

# A function used to convert MD to HTML
def MdToHtml(title):
    markdowner = Markdown()
    entryContent = util.get_entry(title)

    if entryContent != None:
        return markdowner.convert(entryContent)
    else:
        return None

# A function for the index.html page
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# A function for the wiki/TITLE page
def entry(request, title):
    
    entryContent = MdToHtml(title)

    if entryContent != None:
        return render(request, "encyclopedia/entry.html", {
            "entryContent": entryContent
        })

    else:
        return render(request, "encyclopedia/error.html", {
            "title": title
        })

# A function for searching in all pages
def search(request):
    if request.method == "POST":
        entryName = request.POST["q"]
        entryContent = MdToHtml(entryName)

        if entryContent != None:
            return render(request, "encyclopedia/entry.html", {
                "entryContent": entryContent
            })
        
        else:

            entries = util.list_entries()
            results = []

            for entry in entries:
                if entryName.lower() in entry.lower():
                    results.append(entry)
            
            return render(request, "encyclopedia/search.html", {
                "results": results
            })


def NewPage(request):
    if request.method == "POST":
        return
    
    else:
        return render(request, "encyclopedia/new.html")