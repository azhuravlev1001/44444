# Django
from django_filters import CharFilter, FilterSet, NumberFilter

# Yamdb
from reviews.models import Title


class TitleFilter(FilterSet):
    """Класс фильтрации для произведений"""

    category = CharFilter(field_name='category__slug')
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')
    name = CharFilter(field_name='name', lookup_expr='contains')
    year = NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = '__all__'
