from django.db import models
from django.conf import settings

from catalog.models import Book

class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"Cart #{self.id}"
    
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'book')
