from django_filters import FilterSet, CharFilter
from hack.models import SocialContent, Author


class ContentFilter(FilterSet):
    unique_id = CharFilter(lookup_expr='exact')
    platform = CharFilter(lookup_expr='exact')
    main_text = CharFilter(lookup_expr='contains')
    author_id = CharFilter(field_name='author__unique_id', lookup_expr='exact')
    author_username = CharFilter(field_name='author__username', lookup_expr='exact')

    class Meta:
        model = SocialContent
        fields = ['unique_id', 'platform', 'main_text', 'author_id',]