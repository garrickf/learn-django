from django.shortcuts import render
from django.http import HttpResponse # used for debugging
from .models import Book, BookInstance, Author, Language, Genre # models

# Create your views here.
# GF: a view takes a request object and any extra params pulled from the url 
# in our URLconfs. Then, we operate on the data (query the database) and return
# a formatted http response (we can use render to render a template)
def index(request):
    """
    View function for the home page of the site.
    """
    # Generate counts for some of the objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # the all() is implied by default
    # GF: note how we query from the objects and can perform various filters and sorts on the ORM models Django provides

    # Extra: more queries
    num_genres = Genre.objects.count()
    num_books_containing_pastoralia = Book.objects.filter(title__icontains="pAstoralia").count()

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',
        context={'num_books':num_books,
        'num_instances':num_instances,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors, 
        'num_genres':num_genres,
        'num_books_containing_pastoralia':num_books_containing_pastoralia},
    )

    # return HttpResponse('<p>Hello, world!</p>') # DEBUG LINE
