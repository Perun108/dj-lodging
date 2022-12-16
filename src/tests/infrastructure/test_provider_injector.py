import pytest
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from djlodging.infrastructure.providers import DummyProvider
from djlodging.infrastructure.providers.provider_injector import get_provider


class TestProviderInjector:
    def test_get_dummy_provider_succeeds(self):
        setattr(settings, "DUMMY_PROVIDER", "djlodging.infrastructure.providers.DummyProvider")
        provider = get_provider("DUMMY_PROVIDER")
        assert isinstance(provider, DummyProvider)

    def test_get_non_existent_fake_provider_succeeds(self, mocker):
        setattr(settings, "FAKE_PROVIDER", "djlodging.infrastructure.providers.FakeProvider")
        # It's possible to use a context manager with unittest's mock (may be a cleaner solution),
        # but I decided not to mix unittest and pytest and went ahead with mocker,
        # which does not support context manager, unfortunately.
        # with mock.patch.dict("sys.modules", {"djlodging.infrastructure.providers": mock.Mock()}):
        #     provider = get_provider("FAKE_PROVIDER")
        mocker.patch.dict("sys.modules", {"djlodging.infrastructure.providers": mocker.Mock()})
        provider = get_provider("FAKE_PROVIDER")

        assert provider is not None
        assert isinstance(provider, mocker.Mock)

    def test_get_provider_succeeds_1(self):
        provider = get_provider("EMAIL_PROVIDER")
        email_provider = import_string(settings.EMAIL_PROVIDER)
        assert isinstance(provider, email_provider)

    def test_get_provider_succeeds_2(self):
        provider = get_provider("PAYMENT_PROVIDER")
        payment_provider = import_string(settings.PAYMENT_PROVIDER)
        assert isinstance(provider, payment_provider)

    def test_get_provider_fails_with_missing_settings(self):
        with pytest.raises(ImproperlyConfigured) as exc:
            provider = get_provider("UNKNOWN_PROVIDER")  # noqa
        assert str(exc.value) == "Requested setting UNKNOWN_PROVIDER, but it's not configured."

    def test_get_provider_fails_with_missing_provider_class(self):
        with pytest.raises(ImproperlyConfigured) as exc:
            provider = get_provider("FAKE_PROVIDER")  # noqa
        assert str(exc.value) == "Could not import FakeProvider. Did you configure it?"
