from django.contrib import admin

from .models import Category, Tag, Post, PostImage


class PostImageInline(admin.TabularInline):
    model = PostImage
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    inlines = [PostImageInline]


admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
