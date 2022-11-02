from django.db.models import QuerySet


def sort_queryset(queryset: QuerySet, query_params: dict) -> QuerySet:
    ordering_args: str = query_params.get("order_by", None)
    if not ordering_args:
        return queryset
    ordering_args_list = ordering_args.split(",")
    return queryset.order_by(*ordering_args_list)
