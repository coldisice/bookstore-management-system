from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    publication_date = models.DateField()
    cover_image = models.ImageField(
        upload_to='books/',
        blank=True,
        null=True
    )

    authors = models.ManyToManyField(
        Author,
        related_name='books'
    )

    categories = models.ManyToManyField(
        Category,
        related_name='books'
    )

    def __str__(self):
        return self.title
    
# class BookAuthor(models.Model):
#     book = models.ForeignKey(
#         Book,
#         on_delete=models.CASCADE
#     )

#     author = models.ForeignKey(
#         Author,
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         unique_together = ('book', 'author')

# class BookCategory(models.Model):
#     book = models.ForeignKey(
#         Book,
#         on_delete=models.CASCADE
#     )

#     category = models.ForeignKey(
#         Category,
#         on_delete=models.CASCADE
#     )

#     class Meta:
#         unique_together = ('book', 'category')
#         verbose_name = 'Book category'
#         verbose_name_plural = 'Book categories'
