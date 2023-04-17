from django.contrib import admin
from .models import Article, Author, Comment


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass



