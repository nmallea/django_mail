from django.shortcuts import render
from django.shortcuts import redirect
from random import choice
from markdown2 import markdown
from . import util

# entry page view
def entry(request, title):
    content = util.get_entry(title)
    if content == None:
        return render(request, "encyclopedia/error.html", {
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content)
    })

# home page view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# Entry page view
def view(request, title):
    content = util.get_entry(title)
    if not content:
        return render(request, "encyclopedia/error.html", {
            "message": "\"" + title + "\" has not been added yet."
        })
    return render(request, "encyclopedia/view.html", {
        "title": title,
        "content": markdown(content)
    })

# search entry page
def search(request):
    search_request = request.GET.get("q")
    content = util.get_entry(search_request)
    if not content:
        result = []
        for title in util.list_entries():
            if search_request.casefold() in title.casefold():
                result.append(title)
        return render(request, "encyclopedia/search.html", {
            "result": result
        })
    return render(request, "encyclopedia/entry.html", {
        "title": search_request,
        "content": markdown(content)
    })

# create a new entry form
def create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        for entry in util.list_entries():
            if title.casefold() == entry.casefold():
                return render(request, "encyclopedia/create.html", {
                    "message": "This entry already exists!",
                    "title": title,
                    "content": content
                })
        util.save_entry(title, content)
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
        })
    return render(request, "encyclopedia/create.html")

# edit entry page view
def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content": content})

    if request.method == "POST":
        content = request.POST.get("edit_content")
        util.save_entry(title, content)
        return redirect("entry", title)

# using random choice to render random entry page
def random(request):
    title = choice(util.list_entries())
    content = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content)
    })
