from rest_framework import serializers


from .models import (
    Author,
    Book,
    Genre
    )


class AuthorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        exclude = ('slug',)

    def validate(self, attrs):
        author = attrs.get('name')
        if Author.objects.filter(name=author).exists():
            raise serializers.ValidationError(
                'This author already exists'
            )
        return attrs
    

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'slug']


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ('slug',)

    def validate(self, attrs):
        book = attrs.get('title')
        if Book.objects.filter(title=book).exists():
            raise serializers.ValidationError(
                'This book already exists'
            )
        return attrs
    

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'slug']


class BookRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class GenreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['genre']

    def validate(self, attrs):
        genre = attrs.get('genre')
        if Genre.objects.filter(genre=genre).exists():
            raise serializers.ValidationError(
                'Such genre already exists'
            )
        return attrs


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreRetrieveSerializer(serializers.ModelSerializer):
    books = BookListSerializer(read_only=True, many=True)

    class Meta:
        model = Genre
        fields = ['genre', 'books']

    def to_representation(self, instance: Genre):
        books = instance.book_genre.all()
        rep = super().to_representation(instance)
        rep['books'] = BookListSerializer(
            instance=books, many=True).data
        return rep