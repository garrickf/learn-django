from django.shortcuts import render
from django.http import HttpResponse # used for debugging
from .models import Book, BookInstance, Author, Language, Genre # models
from django.views import generic

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

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    # can overrride get context data or get queryset to change the context passed to the view, or change the query

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author

class AuthorDetailView(generic.DetailView):
    model = Author

    def get_context_data(self, **kwargs):
        # Call the base implementation first
        context = super(AuthorDetailView, self).get_context_data(**kwargs)

        # Put in some extra info. The args passed in are in the kwargs variable. (HTTP params are in the self.request.GET.)
        # print('pk:', self.kwargs['pk']) # DEBUG LINE

        # Lookups can span relationships (like table joins) using double underscores that follow the relationships. pk or id seem to be OK!
        books_by_author = Book.objects.filter(author__pk=self.kwargs['pk'])
        # print(books_by_author) # DEBUG LINE
        context['books_by_author'] = books_by_author
        return context