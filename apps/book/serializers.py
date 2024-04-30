from rest_framework import serializers
from django.db.models import Avg

from .models import (
    Author,
    Book,
    Genre
    )
from apps.review.serializers import (
    CommentSerializer,
    LikeSerializer
)


class AuthorCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Author
        exclude = ('slug',)

    def validate(self, attrs):
        author = attrs.get('name')
        if Author.objects.filter(name=author).exists():
            raise serializers.ValidationError(
                'This author already exists'
            )
        user = self.context['request'].user                   
        attrs['user'] = user
        return attrs
    

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author 
        fields = ['first_name', 'last_name', 'slug', 'user']  


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Author
        fields = '__all__'

    def validate(self, attrs):                                  
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class BookCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') 
    
    class Meta:
        model = Book
        exclude = ('slug',)

    def validate(self, attrs: dict):
        book = attrs.get('title')
        if Book.objects.filter(title=book).exists():
            raise serializers.ValidationError(
                'This book already exists'
            )
        user = self.context['request'].user                 
        attrs['user'] = user
        return attrs
    

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book  
        fields = ['title', 'author', 'slug', 'user']       


class BookUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  

    class Meta:
        model = Book                                          
        fields = ['title', 'author', 'desc', 'image', 'year_publ', 'pages', 'slug', 'status', 'book', 'genre', 'user']
    
    def validate(self, attrs):                                 
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class BookRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   

    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):                                 
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)

        rep['comments'] = CommentSerializer(
        instance.books_comments.all(), many=True
        ).data

        rating = instance.books_ratings.aggregate(Avg('rating'))['rating__avg']   
        if rating:
            rep['rating'] = round(rating, 1) 
        else:
            rep['rating'] = 0.0
        
        rep['likes'] = instance.books_likes.all().count()
        rep['liked_by'] = LikeSerializer(
            instance.books_likes.all().only('user'), many=True).data 

        return rep


class GenreCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   

    class Meta:
        model = Genre
        fields = ['genre', 'user']                             

    def validate(self, attrs):
        genre = attrs.get('genre')
        if Genre.objects.filter(genre=genre).exists():
            raise serializers.ValidationError(
                'Such genre already exists'
            )
        user = self.context['request'].user                    
        attrs['user'] = user
        return attrs


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    
    books = BookListSerializer(read_only=True, many=True)

    class Meta: 
        model = Genre  
        fields = ['user', 'genre', 'books']                     

    def to_representation(self, instance: Genre):
        books = instance.book_genre.all()
        rep = super().to_representation(instance)
        rep['books'] = BookListSerializer(
            instance=books, many=True).data
        return rep
    
    def validate(self, attrs):                                   
        user = self.context['request'].user
        attrs['user'] = user
        return attrs