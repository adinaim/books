from django.contrib import admin
from .models import (
    BookPurchase, 
    OrderItems
)


admin.site.register(BookPurchase)
admin.site.register(OrderItems)