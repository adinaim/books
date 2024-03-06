# Generated by Django 5.0.1 on 2024-03-04 11:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0002_alter_author_user_alter_book_user_alter_genre_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BookComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_comments', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_likes', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BookRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(blank=True, choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books_ratings', to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'book')},
            },
        ),
    ]
