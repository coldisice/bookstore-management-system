from django.contrib import admin

from .models import(
    Author,
    Category,
    Book
    # BookAuthor,
    # BookCategory
)

admin.site.register(Author)
admin.site.register(Category)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'price',
        'stock_quantity',
        'publication_date'
    )

    search_fields = (
    'title',
    'isbn'
    )

    list_filter = (
    'publication_date',
    'categories'
    )

    ordering = (
    'title',
    )
# admin.site.register(BookAuthor)
# admin.site.register(BookCategory)