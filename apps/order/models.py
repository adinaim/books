from django.db import models
from django.contrib.auth import get_user_model

from apps.book.models import Book


User = get_user_model()


class BookPurchase(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('finished', 'Finished')
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.RESTRICT,
        related_name='orders'
    )
    book = models.ManyToManyField(
        to=Book,
        through='OrderItems',
    )
    order_id = models.CharField(max_length=58, blank=True)
    total_sum = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Order # {self.order_id}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_id:
            self.order_id = str(self.user.username) + str(self.created_at)[11:19]  #
        return self.order_id
    
    class Meta:
        verbose_name = 'Book order'
        verbose_name_plural = 'Books orders'


class OrderItems(models.Model):
    order = models.ForeignKey(
        to=BookPurchase,
        on_delete=models.RESTRICT, 
        related_name='items'  #
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.RESTRICT,
        related_name='items'   #
    )
    book_num = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Basket item'
        verbose_name_plural = 'Basket items'