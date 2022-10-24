from typing import Optional

from django.db.models import QuerySet
from django_filters.filterset import FilterSetMetaclass


class Filter:
    def __init__(self, filter_set: FilterSetMetaclass) -> None:
        self._filter_set_class = filter_set

    def filter(self, query_params: dict, queryset: Optional[QuerySet] = None) -> QuerySet:
        fs = self._filter_set_class(query_params, queryset=queryset)
        return fs.qs
