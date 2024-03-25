from django.shortcuts import render

# Create your views here.
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import MovieForm
from .models import Movie, Genre


# Create your views here.
def index(request):
    movie = Movie.objects.all()

    context = {
        'movie_list': movie

    }
    return render(request, 'index.html', context)


def detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, "detail.html", {'movie': movie})

from django.http import Http404

@login_required
def add_movie(request):
    if request.method == "POST":
        title = request.POST.get('title')
        poster = request.FILES['poster']
        description = request.POST.get('description')
        release_date = request.POST.get('release_date')
        cast = request.POST.get('cast')
        genre_id = request.POST.get('genre')
        user = request.user  # Get the current logged-in user

        genre = Genre.objects.get(id=genre_id)

        new_movie = Movie.objects.create(
            title=title,
            poster=poster,
            description=description,
            release_date=release_date,
            cast=cast,
            genre=genre,
            added_by=user,  # Associate the movie with the current user
        )

        ytube_trailer = request.POST.get('ytube_trailer')
        new_movie.ytube_trailer = ytube_trailer  # Set ytube_trailer separately
        new_movie.save()

        return redirect('/')
    else:
        genres = Genre.objects.all()
        return render(request, 'add.html', {'genres': genres})

@login_required
def update(request, id):
    try:
        movie = Movie.objects.get(id=id)
        # Check if the current user is the one who added the movie
        if request.user == movie.added_by:
            form = MovieForm(request.POST or None, request.FILES, instance=movie)
            if form.is_valid():
                form.save()
                return redirect('/')
            return render(request, 'edit.html', {'form': form, 'movie': movie})
        else:
            raise Http404("You do not have permission to edit this movie.")
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist.")

@login_required
def delete(request, id):
    try:
        movie = Movie.objects.get(id=id)
        # Check if the current user is the one who added the movie
        if request.user == movie.added_by:
            if request.method == "POST":
                movie.delete()
                return redirect('/')
            return render(request, 'delete.html')
        else:
            raise Http404("You do not have permission to delete this movie.")
    except Movie.DoesNotExist:
        raise Http404("Movie does not exist.")


def genre_list(request):
    genres = Genre.objects.all()
    return render(request, 'genre_list.html', {'genres': genres})

def movies_by_genre(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movies = Movie.objects.filter(genre=genre)
    return render(request, 'movies_by_genre.html', {'genre': genre, 'movies': movies})

def movie_detail(request, genre_slug, movie_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    movie = get_object_or_404(Movie, slug=movie_slug, genre=genre)
    return render(request, 'movie_detail.html', {'genre': genre, 'movie': movie})

def search_results(request):
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = []
    return render(request, 'search_results.html', {'movies': movies, 'query': query})

