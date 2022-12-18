# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
    TitleGenre,
    User,
)


class CustonUserAdmin(UserAdmin):
    list_display = (*UserAdmin.list_display, 'role')


class GenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")


class TitleAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "year", "description", "category")


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("pk", "text", "title", "author", "score", "pub_date")


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "genre")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("pk", "review", "author", "text", "pub_date")


admin.site.register(User, CustonUserAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(TitleGenre, TitleGenreAdmin)
admin.site.register(Comment, CommentAdmin)
