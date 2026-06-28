from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path
from django.conf import settings
from django.http import FileResponse

from pathlib import Path

from io import BytesIO

from .models import Author, Category, Book

from .forms import ImportBooksForm
from .services import (
    import_books_from_excel,
    export_books_to_excel
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

    def export_books(self, request):

        workbook = export_books_to_excel()

        file = BytesIO()
        workbook.save(file)
        file.seek(0)

        return FileResponse(
            file,
            as_attachment=True,
            filename="books.xlsx",
            content_type=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
        )

    def import_books(self, request):

        if request.method == "POST":

            form = ImportBooksForm(
                request.POST,
                request.FILES
            )

            if form.is_valid():

                try:

                    result = import_books_from_excel(
                        form.cleaned_data["excel_file"]
                    )

                    messages.success(
                        request,
                        (
                            f"Импорт завершен. "
                            f"Книг: {result['books']}, "
                            f"Авторов: {result['authors']}, "
                            f"Категорий: {result['categories']}."
                        )
                    )

                    return redirect("..")

                except Exception as error:

                    messages.error(
                        request,
                        str(error)
                    )
        else:
            form = ImportBooksForm()

        context = {
            **self.admin_site.each_context(request),
            "form": form,
            "title": "Импорт книг из Excel"
        }

        return render(
            request,
            "admin/catalog/book/import.html",
            context
        )

    def download_template(self, request):

        file_path = (
            Path(settings.BASE_DIR)
            / "catalog"
            / "templates"
            / "catalog"
            / "static"
            / "catalog"
            / "templates"
            / "books_import_template.xlsx"
        )

        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename="books_import_template.xlsx"
        )

    def get_urls(self):
        urls = super().get_urls()

        custom_urls = [
            path(
                "import/",
                self.admin_site.admin_view(
                    self.import_books
                ),
                name="catalog_book_import"
            ),
            path(
                "import/template",
                self.admin_site.admin_view(self.download_template),
                name="catalog_book_import_template"
            ),
            path(
                "export/",
                self.admin_site.admin_view(self.export_books),
                name="catalog_book_export"
            )
        ]

        return custom_urls + urls
# admin.site.register(BookAuthor)
# admin.site.register(BookCategory)
