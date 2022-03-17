from django.contrib import admin

from .models import Post, Comment, Upvoter

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class UpvoterInline(admin.StackedInline):
    model = Upvoter
    extra = 5

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Content',               {'fields': ['title', 'content']}),
        ('Date information', {'fields': ['pub_date']}),
        ('Upvotes', {'fields': ['upvotes']}),
    ]
    inlines = [CommentInline, UpvoterInline]

admin.site.register(Post, PostAdmin)
