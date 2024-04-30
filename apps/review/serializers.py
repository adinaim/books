from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import (
    BookComment,
    BookRating,
    BookLike,
    SavedBook,
)


User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(
        default=serializers.CurrentUserDefault(),
        source='user.username'
    )

    class Meta:
        model = BookComment
        exclude = ['id']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = BookLike
        fields = ('user', 'book')

    def create(self, validated_data):
        user = self.context.get('request').user
        book = self.context.get('book')
        like = BookLike.objects.filter(user=user, book=book).first()
        if like:
            raise serializers.ValidationError('already liked')
        return super().create(validated_data)

    def unlike(self):
        user = self.context.get('request').user
        book = self.context.get('book')
        like = BookLike.objects.filter(user=user, book=book).first()
        if like:
            like.delete()
        else:
            raise serializers.ValidationError('not liked yet')
    
    # def validate(self, attrs):
    #     user = self.context.get('request').user
    #     attrs['user'] = user
    #     return attrs


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = BookRating
        fields = ('rating', 'user', 'book')

    def validate(self, attrs):
        user = self.context.get('request').user
        attrs['user'] = user
        rating = attrs.get('rating') 
        if rating not in (1, 2, 3, 4, 5):
            raise serializers.ValidationError('Incorrect value. The rating should be between 1 and 5.')
        # if rating:
        #     raise serializers.ValidationError('already exists')
        return attrs

    def update(self, instance, validated_data):
        instance.rating = validated_data.get('rating')
        instance.save()
        return super().update(instance, validated_data)


class SavedBookSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = SavedBook
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        book = request.get('book')
        favorite = SavedBook.objects.filter(user=user, book=book).first()
        if not favorite:
            return super().create(validated_data)
        raise serializers.ValidationError('This book has been saved')

    def del_favorite(self, validated_data):
        user = self.context.get('request').user
        request = self.context.get('request').data
        book = request.get('book').slug
        favorite = SavedBook.objects.filter(user=user, book=book).first()
        if favorite:
            favorite.delete()
        else:
            raise serializers.ValidationError('This book has not been saved')