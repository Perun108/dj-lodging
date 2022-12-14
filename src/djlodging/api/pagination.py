from django.conf import settings
from django.db.models import QuerySet


def paginate_queryset(queryset: QuerySet, query_params: dict) -> dict:
    """
    Provides custom pagination schema for all lis APIs.

    Accepts two query parameters:

    page: A numeric value indicating the page number.
    page_size: A numeric value indicating the page size.

    Returns:
    dict with count:int and results:list.
    """
    count = queryset.count()
    page_size = int(query_params.get("page_size", settings.REST_FRAMEWORK["DEFAULT_PAGE_SIZE"]))
    page = int(query_params.get("page", 1))
    bottom = (page - 1) * page_size
    top = bottom + page_size
    results = queryset[bottom:top]
    return {"count": count, "results": results}
