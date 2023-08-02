from django.shortcuts import render, redirect
import markdown
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request,'encyclopedia/error.html', {
            "title":title,
            'message':'Page not found'
        })
    content_html = markdown.markdown(content)
    return render(request, 'encyclopedia/entry_page.html',{
        'title':title,
        'content':content_html
    })

def search_results(request):
    query = request.GET.get('q')
    entries = util.list_entries()

    matching_entries= [entry for entry in entries if query.lower() in entry.lower()]

    if query in entries:
        return redirect( 'entry_page', title=query)
    
    return render (request, 'encyclopedia/search_results.html',{
        'query':query,
        'entries':matching_entries
    })

def create_new_page(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title in util.list_entries():
            return render (request ,'encyclopedia/error.html', {
                'title':title,
                'message':'Title already has been used'
            })
        util.save_entry(title,content)
        return redirect('entry_page', title=title)


    return render(request, 'encyclopedia/create_new_page.html')        


def edit_page(request, title):
    content = util.get_entry(title)

    if request.method == 'POST':
        content = request.POST.get('content')
        util.save_entry(title,content)
        return redirect('entry_page', title=title)
    return render (request, 'encyclopedia/edit_page.html', {
        'title':title,
        'content':content
    })

def random_page(request):
    
    all_entries = util.list_entries()

    random_entry = random.choice(all_entries)


    return redirect('entry_page', title=random_entry)

