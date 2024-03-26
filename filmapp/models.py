from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Genre(models.Model):
    title = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        ordering = ('title',)
        verbose_name = 'genre'
        verbose_name_plural = 'genres'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('filmapp:movies_by_genre', args=[self.slug])

    def __str__(self):
        return self.title

class Movie(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)
    poster = models.ImageField(upload_to='posters/', null=True, blank=True)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    cast = models.TextField(blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    ytube_trailer = models.URLField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)





    class Meta:
        ordering = ('title',)
        verbose_name = 'movie'
        verbose_name_plural = 'movies'

    def get_absolute_url(self):
        return reverse('filmapp:movie_detail', args=[self.genre.slug, self.slug])

    def __str__(self):
        return self.title
