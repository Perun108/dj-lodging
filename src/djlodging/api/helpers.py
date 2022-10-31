from djlodging.api.exceptions import InvalidQueryParams


def validate_required_query_params_with_any(required_params: list, query_params: dict):
    if set(required_params).isdisjoint(set(query_params)):
        raise InvalidQueryParams(required_params)
