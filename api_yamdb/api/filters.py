# Django
from django_filters import CharFilter, FilterSet

# Yamdb
from reviews.models import Title


class TitleFilter(FilterSet):
    """Класс фильтрации для произведений"""

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
