from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown 
from . import util
from django import forms
from django.utils.safestring import mark_safe
import random

# A function used to convert MD to HTML
def MdToHtml(title):
    markdowner = Markdown()
    entryContent = util.get_entry(title)

    if entryContent != None:
        return markdowner.convert(entryContent)
    else:
        return None

# A function to display an error message
def showError(request, message):
    return render(request, "encyclopedia/error.html", {
            "error": message
        })

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
            "entryContent": entryContent,
            "title": title
        })

    else:
        return showError(request, f"\"{title}\" doesn't exist")

# A function for searching in all pages
def search(request):
    if request.method == "POST":
        entryName = request.POST["q"]
        entryContent = MdToHtml(entryName)

        if entryContent != None:
            return render(request, "encyclopedia/entry.html", {
                "title": entryName,
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

    else:
        return HttpResponseRedirect(reverse("index"))

# A class for all the inputs required to make a new page
class entryinputs(forms.Form,):
    title = forms.CharField(label="Title\n" , widget=forms.TextInput(attrs={"style":"display:block;"}))
    content = forms.CharField(label="Content\n" ,widget=forms.Textarea(attrs={"style":"width: 90%; height:60%; display:block"}))

# A function to add a new entry to the website 
def NewPage(request):
    if request.method == "POST":
        form = entryinputs(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if util.get_entry(title):
                return showError(request, f"The title: \"{title}\" is already taken")
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

        return render(request, "encyclopedia/new.html", {
            "inputs": entryinputs()
        })
    
    else:
        return render(request, "encyclopedia/new.html", {
            "inputs": entryinputs()
        })

# A fucntion to edit existing entries
def EditPage(request, title):
    content = util.get_entry(title)
    if content != None:
        
        if request.method == "POST":
            entryNewContent = request.POST["content"]
            util.save_entry(title, entryNewContent)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))

        else:
            return render(request, "encyclopedia/edit.html",{
                "title": title,
                "content": content
            })
        
    else: 
        return showError(request, f"{title} is an Entry that doesn't exist.")
        
# A function that takes you to a random entry
def RandomEntry(request):
    entries = util.list_entries()
    title = random.choice(entries)
    
    return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))


