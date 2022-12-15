# Django
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import CharField, IntegerField, ChoiceField, ModelSerializer

from .models import Comment, Review, Title


class ReviewSerializer(ModelSerializer):
    author = SlugRelatedField(read_only=True, slug_field='username')
    score = ChoiceField(choices=range(1, 11))
    text = CharField(max_length=500)

    def validate(self, data):
        user = self.context['request'].user
        title = data['title']
        if Review.objects.filter(author=user, title=title):
            raise ValidationError(
                'Отзыв на это произведение уже есть'
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


class TitleSerializer(ModelSerializer):
    rating = IntegerField(source='get_rating', read_only=True)

    class Meta:
        model = Title
        fields = ('name', 'year', 'description', 'genre', 'category', 'rating')
