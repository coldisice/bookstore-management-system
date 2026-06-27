from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Book, Category


def book_list(request):
    categories = Category.objects.all()
    search_query = request.GET.get('q', '')
    category_ids = request.GET.getlist('category')
    category_ids = [
        category_id
        for category_id in category_ids
        if category_id
    ]

    books = Book.objects.all()

    if category_ids:
        books = books.filter(
            categories__id__in=category_ids
        ).distinct()

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query)
        )

    paginator = Paginator(
        books,
        6
    )

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': books,
        'search_query': search_query,
        'categories': categories,
        'selected_categories': category_ids,
        'page_obj': page_obj,
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
