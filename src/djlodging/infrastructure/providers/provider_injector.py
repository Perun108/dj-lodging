from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string


def get_provider(provider_settings_name: str):
    try:
        provider_path: str = getattr(settings, provider_settings_name)
    except AttributeError:
        raise ImproperlyConfigured(
            f"Requested setting {provider_settings_name}, but it's not configured."
        )

    try:
        provider = import_string(provider_path)
    except ImportError:
        raise ImproperlyConfigured(
            f"Could not import {provider_path.split('.')[-1]}. Did you configure it?"
        )
    return provider()
