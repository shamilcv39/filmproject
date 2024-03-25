from django.contrib import admin
from .models import Movie, Genre
from .forms import MovieAdminForm

class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Genre, GenreAdmin)

class MovieAdmin(admin.ModelAdmin):
    form = MovieAdminForm
    list_display = ['title', 'poster', 'description', 'release_date', 'cast', 'genre', 'ytube_trailer']
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 20
admin.site.register(Movie, MovieAdmin)

# Register your models here.
