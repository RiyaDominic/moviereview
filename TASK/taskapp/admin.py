from django.contrib import admin
from .models import Category, Movie,Review

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'created', 'updated']  # Include 'description' in list_display
    list_editable = ['category']  # Make 'description' editable
    list_display_links = ['name']  # Set 'name' as a link
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Movie, MovieAdmin)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating']
    prepopulated_fields = {'rating': ('name',)}
admin.site.register(Review)

