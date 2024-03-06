from rest_framework.permissions import (
    IsAuthenticated,
)

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import(
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
)
from rest_framework.response import Response
from rest_framework import mixins

from apps.book.permissions import IsOwner
from apps.book.models import Book

from .serializers import (
    RatingSerializer,
    CommentSerializer,
    LikeSerializer,
    SavedBookSerializer
)
from .models import (
    BookComment, 
    BookLike,
    BookRating,
    SavedBook
)


class SavedBookViewSet(mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    queryset = SavedBook.objects.all()
    serializer_class = SavedBookSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'save' and self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'save' and self.request.method =='DELETE':
            self.permission_classes = [IsOwner]
        # if self.action == 'list':
        #     self.permission_classes = [IsOwner]
        return super().get_permissions()

    def save(self, request, pk=None):
        book = self.get_object().get('slug')
        serializer = SavedBookSerializer(
            data=request.data, 
            context={
                'request':request,
                'book':book
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('This book has been saved')
            if request.method == 'DELETE':
                        serializer.del_favorite()
                        return Response('This book has been removed from savings')


class BookCommentView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = BookComment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RatingView(mixins.CreateModelMixin,
                mixins.DestroyModelMixin,
                mixins.ListModelMixin,
                GenericViewSet):
    queryset = BookRating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class LikeView(mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    serializer_class = LikeSerializer
    queryset = BookLike.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_permissions(self):
        if self.action == 'like' and self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated]
        if self.action == 'like' and self.request.method =='DELETE':
            self.permission_classes = [IsOwner]
        return super().get_permissions()

    def like(self, request, pk=None):
        book = self.get_object()
        serializer = LikeSerializer(
            data=request.data, 
            context={
                'request':request,
                'book':book
            })
        if serializer.is_valid(raise_exception=True):
            if request.method == 'POST':
                serializer.save(user=request.user)
                return Response('liked!')
            if request.method == 'DELETE':
                serializer.unlike()
                return Response('unliked!')
