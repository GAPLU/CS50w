from django.shortcuts import render
from markdown2 import Markdown
from django import forms
from random import randint
from django.shortcuts import redirect


from . import util

markdowner = Markdown()

class PageForm(forms.Form):
    title = forms.CharField(label="Search Titile")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    markdown = util.get_entry(title)
    if markdown:
        html = markdowner.convert(markdown)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": html
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "This page doesn't exist yet"
        })
    
def search(request):
    title = request.GET.get('q')
    if title:
        markdown = util.get_entry(title)
        if markdown:
            return redirect('entry', title=title)
        else:
            results = []
            entries = util.list_entries()
            for entry in entries:
                if title.lower() in entry.lower():
                    results.append(entry)
            if results:
                return render(request, "encyclopedia/search.html", {
                    "entries": results
                })
            else:
                return render(request, "encyclopedia/error.html", {
                    "message": "No results found"
                })
    else:
        return render(request, "encyclopedia/error.html", {
            "message": "No results found"
        })
    
def new_page(request):
    if request.method == "POST":
        title = request.POST.get("page_title")
        if title in util.list_entries():
            return render(request, "encyclopedia/error.html", {
            "message": "Article already exists"
            })
        content = request.POST.get("page_content")
        if content.strip():
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "You should provide some input"
            })
    else:
        return render(request, "encyclopedia/new_page.html")
    

def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get("page_content")
        content = clean_text(content)
        if content.strip():
            content = content.strip()
            util.save_entry(title, content)
            return entry(request, title)
        else:
            return render(request, "encyclopedia/error.html", {
                "message": "You should provide some input"
            })
    else:
        content = util.get_entry(title)
        content = clean_text(content)
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })
    

def random_page(request):
    entries = util.list_entries()
    num = randint(0, len(entries) - 1)
    result = entries[num]
    return redirect('entry', title=result)

def clean_text(content):
    cleaned = []
    output = ""
    content = content.split("\n")
    for line in content:
        if line.strip():
            cleaned.append(line)
    for clean in cleaned:
        output += f"{clean}\n"
    return output

    
