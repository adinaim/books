from django.db import models
from django.contrib.auth import get_user_model
# from django.urls import reverse


from apps.book.models import Book


User = get_user_model()


class BookComment(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books_comments'
    )
    comment_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment from {self.user.username} to {self.book.title}'


class BookRating(models.Model):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE =5
    RATING_CHOICES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, blank=True, null=True)
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books_ratings'
    )

    def __str__(self) -> str:
        return f'{self.rating} points to {self.book.title}'
    
    class Meta:
        unique_together = ['user', 'book', 'rating']


class BookLike(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='likes',
        null=True
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='books_likes'
    )
    # book_id = models.PositiveSmallIntegerField(null=True, blank=True)

    def __str__(self):
        return f'Liked by {self.user.username}'
    

class SavedBook(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
    )