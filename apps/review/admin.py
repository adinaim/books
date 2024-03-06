from django.contrib import admin
from .models import (
    BookComment, 
    BookRating, 
    BookLike
)


admin.site.register([BookComment, BookRating, BookLike])