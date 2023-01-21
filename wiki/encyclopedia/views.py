from django.shortcuts import render
from markdown2 import Markdown 
from . import util

def MdToHtml(title):
    markdowner = Markdown()
    entryContent = util.get_entry(title)

    if entryContent is not None:
        return markdowner.convert(entryContent)
    else:
        return None

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry():
    return