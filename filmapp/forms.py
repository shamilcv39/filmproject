from django import forms
from .models import Movie, Genre


class MovieForm(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['title','poster','description','release_date','cast','genre','ytube_trailer']


# forms.py

from django import forms
from django.contrib import admin
from .models import Movie

class MovieAdminForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = '__all__'


    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), label='Genre')