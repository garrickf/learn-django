from django.contrib import admin

# Register your models here.
# Models we made in models.py are imported and registered here.
from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class AuthorAdmin(admin.ModelAdmin):
	# list attributes (these are the same one we declared in our model)
	list_display = ('__str__', 'first_name', 'last_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')] # order the fields

admin.site.register(Author, AuthorAdmin)

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0 # no extra instances, any extras we add ourselves.

# can also use a decorator (how does this work? order seems to matter)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre') # note how you can call functions! super handy.
	list_filter = ('genre',) # seems like I can do it by genre too!
	inlines = [BooksInstanceInline] # inlines let us see associated records

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('title', 'id', 'status', 'due_back')
	list_filter = ('status', 'due_back')

	# fieldsets determine how the fields are grouped together and organized
	fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
    )