from django.db import models
from slugify import slugify
from django.contrib.auth import get_user_model


User = get_user_model()


class Author(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField()
    image = models.ImageField(upload_to='author_images')
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)        
    name = models.CharField(max_length=101, blank=True)   

    def save(self, *args, **kwargs):
        if not self.name:                                 
            self.name = self.last_name + ' ' + self.first_name  
        if not self.slug:
            self.slug = slugify(self.name)                      # change
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    STATUS_CHOICES = (             
        ('archive', 'Archived'),
        ('avail', 'Available')
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    title = models.CharField(max_length=70)
    author = models.ForeignKey(
        to=Author,
        related_name='book_authors',
        on_delete=models.CASCADE
    )
    desc = models.CharField(max_length=200)
    image = models.ImageField(upload_to='book_images')
    year_publ = models.CharField(max_length=4)
    pages = models.PositiveIntegerField()
    slug = models.SlugField(primary_key=True, blank=True, max_length=80)
    status = models.CharField(choices=STATUS_CHOICES, max_length=9)       
    book = models.FileField(upload_to='book_files')    
    genre = models.ManyToManyField(
        to='Genre',
        related_name='book_genre'
    )                   
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)   
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Genre(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    genre = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=25)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.genre
    
    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"