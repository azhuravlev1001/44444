from django.db import models
from .categories import Category
from .genres import Genre


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genre, through='TitleGenre')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='categories'
    )

    def __str__(self):
        return self.name
