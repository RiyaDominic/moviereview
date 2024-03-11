
from django import forms
from .models import Movie, Review

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['name', 'description', 'category', 'image', 'release_date', 'actors', 'trailer_link'] 
        exclude = ['user','slug']
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']