from rest_framework.viewsets import ModelViewSet, GenericViewSet   
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
)   

from .models import (
    Author,
    Book,
    Genre     
)
from .permissions import (
    IsOwner
)

from .serializers import (
    AuthorCreateSerializer, 
    AuthorListSerializer, 
    AuthorRetrieveSerializer,
    
    BookCreateSerializer, 
    BookListSerializer, 
    BookUpdateSerializer, 
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
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    

class BookViewSet(ModelViewSet):      
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return BookCreateSerializer
        elif self.action == 'list':
            return BookListSerializer
        elif self.action in ['update', 'partial_update']:
            return BookUpdateSerializer
        elif self.action == 'retrieve':
            return BookRetrieveSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        author_id = request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
        if self.action == 'list': 
            self.permission_classes = [AllowAny]
        elif self.action == 'retrieve': 
            self.permission_classes = [IsAuthenticated]
        elif self.action in ['create', 'update', 'partial_update']: 
            self.permission_classes = [IsAdminUser]
        elif self.action == 'destroy': 
            self.permission_classes = [IsOwner]
        return super().get_permissions()