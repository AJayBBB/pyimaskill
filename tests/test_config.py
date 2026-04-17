from datetime import datetime, timedelta, timezone

import pytest

from pyimaskill.config import Config, load_config


def test_config_requires_credentials():
    with pytest.raises(ValueError, match="client_id and api_key are required"):
        Config(client_id="", api_key="test")

    with pytest.raises(ValueError, match="client_id and api_key are required"):
        Config(client_id="test", api_key="")


def test_config_valid_credentials():
    config = Config(client_id="test_id", api_key="test_key")
    assert config.client_id == "test_id"
    assert config.api_key == "test_key"
    assert config.base_url == "https://ima.qq.com"
    assert config.timeout == 30.0


def test_load_config_explicit_args():
    config = load_config(client_id="explicit_id", api_key="explicit_key")
    assert config.client_id == "explicit_id"
    assert config.api_key == "explicit_key"


def test_validate_credentials_warns_before_expiry():
    now = datetime(2026, 4, 6, tzinfo=timezone.utc)
    config = Config(
        client_id="test_id",
        api_key="test_key",
        api_key_expires_at=now + timedelta(hours=2),
        expiry_warning_window=24 * 60 * 60,
    )

    warnings = config.validate_credentials(now=now)
    assert any("hours" in warning for warning in warnings)


def test_validate_credentials_requires_renewal_for_expired_api_key():
    now = datetime(2026, 4, 6, tzinfo=timezone.utc)
    config = Config(
        client_id="test_id",
        api_key="test_key",
        api_key_expires_at=now - timedelta(minutes=1),
    )

    with pytest.raises(ValueError, match="api_key expired"):
        config.validate_credentials(now=now)


def test_config_build_headers():
    config = Config(client_id="test_id", api_key="test_key")
    headers = config.build_headers()
    assert headers["ima-openapi-clientid"] == "test_id"
    assert headers["ima-openapi-apikey"] == "test_key"
    assert headers["Content-Type"] == "application/json"
    assert "ima-openapi-ctx" in headers
    assert "skill_version=" in headers["ima-openapi-ctx"]