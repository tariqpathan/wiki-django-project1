import markdown2
import random
import re
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError

from . import util
from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    text = forms.CharField(label="Text", widget=forms.Textarea)

    def clean_title(self):
        title = self.cleaned_data["title"]
        if title.lower() in [s.lower() for s in util.list_entries()]:
            raise ValidationError("Title already exists")
        return title

class EditPageForm(forms.Form):
    text = forms.CharField(label="Text", widget=forms.Textarea)
    # populate with existing text

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query = request.GET.get('q')
    entries = util.list_entries()
    
    if query.lower() in map(lambda x:x.lower(), entries):
        return redirect(topic, query)
    else:
        results = [s for s in entries if query.lower() in s.lower()]
    
    return render(request, "encyclopedia/search.html", {
        "results": results
    })

def topic(request, title):
    if util.get_entry(title):
        text = util.get_entry(title)
        match = re.search(r"#\s(\w+(\s\w+)*)", text)
        """ Will get a text file returned - convert markdown to html """
        return render(request, "encyclopedia/topic.html", {
            "title": match.group(1),
            "text": markdown2.markdown(text)
        })
    else:
        return render(request, "encyclopedia/error.html")

def newpage(request):
    if request.method == "POST":
        # form is populated with filled data
        form = NewPageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            # save the entry and redirect to new topic
            return redirect(topic, title)

        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    # GET request
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def randompage(request):
    title = random.choice(util.list_entries())
    return redirect(topic, title)

def editpage(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data["text"]
            util.save_entry(title, text)
            return redirect(topic, title)
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": form
            })
    else:
        text = util.get_entry(title)
        form = EditPageForm(initial={
            "text": text
        })
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "form": form
        })