from django.shortcuts import render
from django.http import HttpResponse # used for debugging

# Create your views here.
# GF: a view takes a request object and any extra params pulled from the url 
# in our URLconfs. Then, we operate on the data (query the database) and return
# a formatted http response (we can use render to render a template)
def index(request) :
	return HttpResponse('<p>Hello, world!</p>')
