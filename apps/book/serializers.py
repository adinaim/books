from rest_framework import serializers


from .models import (
    Author,
    Book,
    Genre
    )


class AuthorCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 1

    class Meta:
        model = Author
        exclude = ('slug',)

    def validate(self, attrs):
        author = attrs.get('name')
        if Author.objects.filter(name=author).exists():
            raise serializers.ValidationError(
                'This author already exists'
            )
        user = self.context['request'].user                   # 1
        attrs['user'] = user
        return attrs
    

class AuthorListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author 
        fields = ['first_name', 'last_name', 'slug', 'user']  # 2


class AuthorRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 3

    class Meta:
        model = Author
        fields = '__all__'

    def validate(self, attrs):                               # 3
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class BookCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username') # 4
    
    class Meta:
        model = Book
        exclude = ('slug',)

    def validate(self, attrs: dict):
        book = attrs.get('title')
        if Book.objects.filter(title=book).exists():
            raise serializers.ValidationError(
                'This book already exists'
            )
        user = self.context['request'].user                 # 4
        attrs['user'] = user
        return attrs
    

class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book  
        fields = ['title', 'author', 'slug', 'user']       # 5


class BookUpdateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # 6

    class Meta:
        model = Book                                          # 6
        fields = ['title', 'author', 'desc', 'image', 'year_publ', 'pages', 'slug', 'status', 'book', 'genre', 'user']
    
    def validate(self, attrs):                                 # 6
        user = self.context['request'].user
        attrs['user'] = user
        return attrs


class BookRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 7

    class Meta:
        model = Book
        fields = '__all__'

    def validate(self, attrs):                                 # 7
        user = self.context['request'].user
        attrs['user'] = user
        return attrs
    
    # def to_representation(self, instance):
    #     rep = super().to_representation(instance)

    #     rep['comments'] = CommentSerializer(
    #     instance.books_comments.all(), many=True
    #     ).data

    #     rating = instance.books_ratings.aggregate(Avg('rating'))['rating__avg']   
    #     if rating:
    #         rep['rating'] = round(rating, 1) 
    #     else:
    #         rep['rating'] = 0.0
        
    #     rep['likes'] = instance.books_likes.all().count()
    #     rep['liked_by'] = LikeSerializer(
    #         instance.books_likes.all().only('user'), many=True).data 

    #     return rep


class GenreCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')   # 8

    class Meta:
        model = Genre
        fields = ['genre', 'user']                             # 8

    def validate(self, attrs):
        genre = attrs.get('genre')
        if Genre.objects.filter(genre=genre).exists():
            raise serializers.ValidationError(
                'Such genre already exists'
            )
        user = self.context['request'].user                    # 8
        attrs['user'] = user
        return attrs


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')    # 9
    books = BookListSerializer(read_only=True, many=True)

    class Meta: 
        model = Genre  
        fields = ['user', 'genre', 'books']                     # 9

    def to_representation(self, instance: Genre):
        books = instance.book_genre.all()
        rep = super().to_representation(instance)
        rep['books'] = BookListSerializer(
            instance=books, many=True).data
        return rep
    
    def validate(self, attrs):                                   # 9
        user = self.context['request'].user
        attrs['user'] = user
        return attrs