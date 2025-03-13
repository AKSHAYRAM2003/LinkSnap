
from django.contrib import admin
from .models import Bookmark, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'user', 'is_favorite', 'created_at')
    list_filter = ('is_favorite', 'created_at', 'tags')
    search_fields = ('title', 'description', 'url')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'
