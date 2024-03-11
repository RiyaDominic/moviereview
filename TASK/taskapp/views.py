from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.contrib import messages
from .models import Category, Movie
from .forms import MovieForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg


def allProdCat(request, c_slug=None):
    c_page = None
    movies_list = None
    if c_slug is not None:
        c_page = get_object_or_404(Category, slug=c_slug)
        movies_list = Movie.objects.filter(category=c_page)
    else:
        movies_list = Movie.objects.all()
    paginator = Paginator(movies_list, 6)
    page = request.GET.get('page', 1)
    try:
        movies = paginator.page(page)
    except (EmptyPage, InvalidPage):
        movies = paginator.page(paginator.num_pages)

    return render(request, "category.html", {'category': c_page, 'movies': movies})

def ProDetail(request, c_slug, movie_slug):
    movie = get_object_or_404(Movie, category__slug=c_slug, slug=movie_slug)
    return render(request, 'movie.html', {'movie': movie})

@login_required
def edit_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user != movie.user:
        messages.error(request, "You don't have permission to edit this movie.")
        return redirect('taskapp:allProdCat')
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('taskapp:allProdCat')  # Redirect to movie listing page
    else:
        movie_form = MovieForm(instance=movie)
    return render(request, 'edit_movie.html', {'movie_form': movie_form, 'movie': movie})
   

@login_required
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.user != movie.user:
        messages.error(request, "You don't have permission to delete this movie.")
        return redirect('taskapp:allProdCat')
    if request.method == 'POST':
        movie.delete()
        messages.success(request, "Movie deleted successfully.")
        return redirect('taskapp:allProdCat')
    return render(request, 'delete_movie.html', {'movie': movie})

def add_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect('taskapp:allProdCat')
    else:
        review_form = ReviewForm()
    return render(request, 'add_review.html', {'review_form': review_form})

def view_reviews(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = movie.reviews.all()
    average_rating = None
    if reviews:
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    for review in reviews:
        review.stars = range(review.rating)
        review.empty_stars = range(5 - review.rating)
    return render(request, 'view_reviews.html', {'movie': movie, 'reviews': reviews,'average_rating':average_rating})
@login_required
def add_movies(request):
    if request.method == "POST":
        movie_form = MovieForm(request.POST, request.FILES)
        if movie_form.is_valid():
            movie = movie_form.save(commit=False)
            movie.user = request.user
            movie.save()
            return redirect('taskapp:add_movie_success')  # Redirect to success page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        movie_form = MovieForm()
    return render(request, "add_movie.html", context={"movie_form": movie_form})

def add_movie_success(request):
    return render(request, "add_movie_success.html")
