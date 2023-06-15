from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre

# Create your views here.

def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_genres_fiction = Genre.objects.filter(name__icontains='Fiction').count()
    num_books_fiction = Book.objects.filter(genre__name__icontains='Fiction').count()
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genres_fiction': num_genres_fiction,
        'num_books_fiction': num_books_fiction,
    }

    return render(request, 'index.html', context=context)