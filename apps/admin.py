from django.contrib import admin
from .models import Category, Post, Comment, Profile  
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'created_at', 'published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published', 'created_at', 'category')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'approved')
    list_filter = ('approved', 'created_at')
    search_fields = ('content', 'author__username') 

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',) 
    
