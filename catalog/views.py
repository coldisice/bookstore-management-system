from django.shortcuts import render, get_object_or_404

from .models import Book

def book_list(request):
    books = Book.objects.all()

    context = {
        'books': books
    }

    return render(
        request,
        'catalog/book_list.html',
        context
    )

def book_detail(request, book_id):
    book = get_object_or_404(
        Book,
        id=book_id
    )

    return render(
        request,
        'catalog/book_detail.html',
        {'book': book}
    )