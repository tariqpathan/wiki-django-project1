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
    text = forms.CharField(label="Text")
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
            "text": text
        })
    else:
        return render(request, "encyclopedia/error.html")

def newpage(request):
    if request.method == "POST":
        # form is populated with filled data
        form = NewPageForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            # entries = util.list_entries()
        
            # if title.lower() in [s.lower() for s in entries]:
            #     raise forms.ValidationError('Title already exists')
            #     # return render(request, "encyclopedia/newpage.html", {
            #     #     "form": form
            #     # })

            # else:
            text = form.cleaned_data["text"]
            print(text)
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
