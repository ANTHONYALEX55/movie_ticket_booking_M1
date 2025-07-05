from django.contrib import admin
from .models import Movie,Cast
# Register your models here.

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'language','release_date',
                    'created_at', 'movie_image','status','trailer_url',
                    'synopsis')
    
@admin.register(Cast)
class CastAdmin(admin.ModelAdmin):
    list_display = ('name','role','image','movie')
    
