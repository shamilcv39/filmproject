from . import views
from django.urls import path



app_name='filmapp'

urlpatterns = [

    path('',views.index,name='index'),
    path('movie/<int:movie_id>/',views.detail,name='detail'),
    path('add/',views.add_movie,name='add_movie'),
    path('update/<int:id>/',views.update,name='update'),
    path('delete/<int:id>/',views.delete,name='delete'),
    path('genres/',views.genre_list, name='genre_list'),
    path('genres/<slug:genre_slug>/', views.movies_by_genre, name='movies_by_genre'),
    path('genres/<slug:genre_slug>/<slug:movie_slug>/', views.movie_detail, name='movie_detail'),
    path('search/', views.search_results, name='search_results'),



]