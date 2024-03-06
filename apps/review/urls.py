from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    SavedBookViewSet,
    BookCommentView,
    RatingView,
    LikeView,
)


router = DefaultRouter()


router.register('saved-book', SavedBookViewSet, 'saved book')
router.register('book-comment', BookCommentView, 'comment')
router.register('book-rating', RatingView, 'rating')
router.register('book-like', LikeView, 'like')


urlpatterns = [

]
urlpatterns += router.urls