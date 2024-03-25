from .models import Genre
def menu_links(request):
    genres = Genre.objects.all()
    return dict(genres=genres)