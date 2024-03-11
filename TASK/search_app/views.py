from django.shortcuts import render
from django.db.models import Q
from taskapp.models import Movie


def SearchResult(request):
    movies = None
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'search.html', {'query': query, 'movies': movies})
