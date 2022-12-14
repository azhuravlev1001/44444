from rest_framework.serializers import ModelSerializer, ChoiceField, CharField
from rest_framework.relations import SlugRelatedField
from .models_alex import Comment, Review, OneTitleOneReview
from rest_framework.exceptions import ValidationError


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    score = ChoiceField(choices=range(1, 11))
    text = CharField(max_length=500)

    def validate(self, data):
        user = self.context['request'].user
        title = data['title']
        if (OneTitleOneReview.objects.filter(user=user, title=title)):
            raise ValidationError(
                'Отзыв на это произведение уже есть'
                # когда будет модель Title, сделать f-строку
                # с указанием конкретного произведения
            )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    text = CharField(max_length=500)

    class Meta:
        model = Comment
        fields = '__all__'
