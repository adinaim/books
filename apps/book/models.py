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
            self.slug = slugify(self.name)                                     # change
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(models.Model):
    GENDER_CHOICES = (             
        ('f', 'Female'),
        ('m', 'Male'),
        ('nb', 'Non binary')
    )

    gender = models.CharField(choices=GENDER_CHOICES, max_length=10)  
    birthday = models.DateField()   
    cashback = models.PositiveSmallIntegerField()
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    user = models.ForeignKey(
        to=User,
        on_delete=models.DO_NOTHING,
    )
    
    def __str__(self):
        return f'{self.user}'
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


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