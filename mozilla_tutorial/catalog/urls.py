from django.urls import path
from . import views

# Patterns for the catalog app
urlpatterns = [
	path('', views.index, name='main-view'),
]