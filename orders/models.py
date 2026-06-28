from django.db import models
from django.conf import settings

from catalog.models import Book


class Order(models.Model):

    class Status(models.TextChoices):
        NEW = 'NEW', 'Новый'
        PROCESSING = "PROCESSING", 'В процессе'
        SHIPPED = 'SHIPPED', 'Передан в доставку'
        COMPLETED = 'COMPLETED', 'Завершен'
        CANCELLED = 'CANCELLED', 'Отменен'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"Заказ №{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.book.title} ({self.quantity})'

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.book.price

        super().save(*args, **kwargs)
