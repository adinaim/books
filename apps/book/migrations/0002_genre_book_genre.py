# Generated by Django 5.0.1 on 2024-02-13 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=25, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='genre',
            field=models.ManyToManyField(related_name='book_genre', to='book.genre'),
        ),
    ]