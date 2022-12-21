from django_filters import (FilterSet, CharFilter, NumberFilter)
from reviews.models import Title


class TitleFilter(FilterSet):
    category = CharFilter(field_name='category__slug',
                          lookup_expr='contains')
    genre = CharFilter(field_name='genre__slug',
                       lookup_expr='contains')
    name = CharFilter(field_name='name',
                      lookup_expr='contains')
    year = NumberFilter(field_name='year',
                        lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year')
