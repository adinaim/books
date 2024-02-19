from rest_framework.viewsets import ModelViewSet, GenericViewSet   
from rest_framework.permissions import AllowAny
from rest_framework import mixins   

from .models import (
    Author,
    Book,
    Genre     
)

from .serializers import (
    AuthorCreateSerializer, 
    AuthorListSerializer, 
    AuthorRetrieveSerializer,
    
    BookCreateSerializer, 
    BookListSerializer, 
    BookRetrieveSerializer,

    GenreCreateSerializer,   
    GenreListSerializer,     
    GenreRetrieveSerializer  
)

class AuthorViewSet(ModelViewSet):      
    queryset = Author.objects.all()
    serializer_class = AuthorCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AuthorCreateSerializer
        elif self.action == 'list':
            return AuthorListSerializer
        elif self.action == 'retrieve':
            return AuthorRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
    

class BookViewSet(ModelViewSet):      # CRUD - Create, Retrieve, Update, Delete, List 
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'list':
            return BookListSerializer
        elif self.action == 'retrieve':
            return BookRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class GenreViewSet(mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return GenreCreateSerializer
        elif self.action == 'list':
            return GenreListSerializer
        elif self.action == 'retrieve':
            return GenreRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'create', 'destroy', 'update', 'partial_update']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()