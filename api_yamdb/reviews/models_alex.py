from django.db.models import (
    Model, TextField, ForeignKey, CASCADE, PositiveSmallIntegerField,
    DateTimeField
)
# from .models import Title, User

STR_LENGTH = 15


class Review(Model):
    text = TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    # title = ForeignKey(
    #     Title,
    #     verbose_name='Произведение',
    #     help_text='Произведение, на которое оставляем отзыв',
    #     on_delete=CASCADE
    # )
    # author = ForeignKey(
    #     User,
    #     on_delete=CASCADE,
    #     verbose_name='Автор отзыва',
    #     help_text='Автор отзыва'
    # )
    score = PositiveSmallIntegerField(
        verbose_name='Оценка отзыва',
        help_text='Оценка отзыва, число от 1 до 10'
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации отзыва',
        auto_now_add=True,
        help_text='Дата публикации отзыва (ставится автоматически)'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:STR_LENGTH]


class Comment(Model):
    review = ForeignKey(
        Review,
        on_delete=CASCADE,
        verbose_name='Комментарий',
        help_text='Комментарий к отзыву'
    )
    # author = ForeignKey(
    #     User,
    #     on_delete=CASCADE,
    #     verbose_name='Автор комментария',
    #     help_text='Автор комментария'
    # )
    text = TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария'
    )
    pub_date = DateTimeField(
        verbose_name='Дата комментария',
        auto_now_add=True,
        help_text='Дата комментария (ставится автоматически)'
    )

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:STR_LENGTH]
