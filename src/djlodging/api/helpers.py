from rest_framework.exceptions import ValidationError as DRFValidationError


class InvalidQueryParams(DRFValidationError):
    def __init__(self, required_params=None):
        message = (
            f"Query params must include at least one of the following parameters {required_params}"
        )
        super().__init__(message)


def validate_required_query_params_with_any(required_params: list, query_params: dict):
    if set(required_params).isdisjoint(set(query_params)):
        raise InvalidQueryParams(required_params)
