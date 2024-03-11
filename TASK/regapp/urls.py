from django.urls import path, include
from . import views

app_name = 'regapp'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]