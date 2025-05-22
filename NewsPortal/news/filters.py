from django_filters import FilterSet, DateFilter
from .models import Post
from django import forms


class PostFilter(FilterSet):
    date_creation = DateFilter(
        field_name='create_time',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte',
    )

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['icontains'],
        }
