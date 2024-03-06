# Generated by Django 5.0.1 on 2024-02-21 06:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('about', models.TextField()),
                ('image', models.ImageField(upload_to='author_images')),
                ('slug', models.SlugField(blank=True, max_length=120, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=101)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=25, primary_key=True, serialize=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('title', models.CharField(max_length=70)),
                ('desc', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='book_images')),
                ('year_publ', models.CharField(max_length=4)),
                ('pages', models.PositiveIntegerField()),
                ('slug', models.SlugField(blank=True, max_length=80, primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('archive', 'Archived'), ('avail', 'Available')], max_length=9)),
                ('book', models.FileField(upload_to='book_files')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_authors', to='book.author')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('genre', models.ManyToManyField(related_name='book_genre', to='book.genre')),
            ],
            options={
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
    ]
