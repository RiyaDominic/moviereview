from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Category(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_url(self):
        return reverse('taskapp:movie_by_category', args=[self.slug])

class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='movie')
    release_date = models.DateField(default='2024-01-01')
    actors = models.CharField(max_length=250,default='')
    trailer_link = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            while Movie.objects.filter(slug=self.slug).exists():
                self.slug = slugify(self.name) + '-' + get_random_string(5)  # Add random suffix
        super().save(*args, **kwargs)

    def get_url(self):
        return reverse('taskapp:prodCatdetail', args=[self.category.slug, self.slug])
    def user_can_edit(self, user):
        
        return user == self.added_by
        
class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        
        