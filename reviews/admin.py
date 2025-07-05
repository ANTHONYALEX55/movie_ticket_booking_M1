from django.contrib import admin
from .models import Review
# Register your models here.

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = [ 'user','movie','rating','review_text','created_at']