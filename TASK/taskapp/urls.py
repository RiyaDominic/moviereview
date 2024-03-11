
from django.urls import path
from . import views

app_name = 'taskapp'

urlpatterns = [
    path('add/',views.add_movies,name='add_movies'),
    path('success/', views.add_movie_success, name='add_movie_success'),
    path('', views.allProdCat, name='allProdCat'),
    path('<slug:c_slug>/', views.allProdCat, name='movie_by_category'),
    path('<slug:c_slug>/<slug:movie_slug>/', views.ProDetail, name='prodCatdetail'),
    path('delete_movie/<int:movie_id>', views.delete_movie, name='delete_movie'),
    path('edit_movie/<int:movie_id>', views.edit_movie, name='edit_movie'),
    path('movie/<int:movie_id>/add_review/', views.add_review, name='add_review'),
    path('movie/<int:movie_id>/view_reviews/', views.view_reviews, name='view_reviews'),
    
    
    
]

