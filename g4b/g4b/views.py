import json
from urllib import quote_plus
import urllib2

from django.shortcuts import render, redirect

from g4b import models

BASE_GOOGLE_API_URL = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="

def home(req):
    form = models.SearchForm(req.GET)
    
    if form.is_valid():
        return results(req, form)
    else:
        form = models.SearchForm()
        return render(req, "search.html", locals())

def results(req, form):
    # Build the URL for the Google JSON api. See http://googlesystem.blogspot.com/2008/04/google-search-rest-api.html
    
    quoted_q = quote_plus(form.cleaned_data['q'])
    
    url = BASE_GOOGLE_API_URL + quoted_q
    
    
    # Fetch the JSON data for the given query
    
    raw_data = urllib2.urlopen(url).read().decode('utf-8')
    
    data = json.loads(raw_data)
    
    return render(req, "results.html", {
        "data" : data,
    })
