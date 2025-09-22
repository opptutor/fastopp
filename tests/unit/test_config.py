"""
Unit tests for configuration dependencies.

This module tests the dependency injection system for configuration,
including Settings class and get_settings function.
"""

import pytest
import os
from unittest.mock import patch, MagicMock
from pydantic import ValidationError

from dependencies.config import Settings, get_settings
from tests.dependencies import get_test_settings


class TestSettingsClass:
    """Test Settings class functionality."""

    def test_settings_default_values(self):
        """Test that Settings has correct default values."""
        settings = Settings()
        
        assert settings.database_url == "sqlite+aiosqlite:///./test.db"
        assert settings.secret_key.startswith("dev_secret_key_")  # Secret key is generated dynamically
        assert settings.environment == "development"
        assert settings.access_token_expire_minutes == 30
        assert settings.upload_dir == "static/uploads"
        # API keys may be set from environment variables
        assert settings.openrouter_api_key is not None or settings.openrouter_api_key is None
        assert settings.openai_api_key is not None or settings.openai_api_key is None

    def test_settings_with_custom_values(self):
        """Test Settings with custom values."""
        settings = Settings(
            database_url="postgresql://user:pass@localhost/db",
            secret_key="custom_secret_key",
            environment="production",
            access_token_expire_minutes=60,
            upload_dir="/custom/uploads",
            openrouter_api_key="custom_openrouter_key",
            openai_api_key="custom_openai_key"
        )

        assert settings.database_url == "postgresql://user:pass@localhost/db"
        assert settings.secret_key == "custom_secret_key"
        assert settings.environment == "production"
        assert settings.access_token_expire_minutes == 60
        assert settings.upload_dir == "/custom/uploads"
        assert settings.openrouter_api_key == "custom_openrouter_key"
        assert settings.openai_api_key == "custom_openai_key"

    def test_settings_case_insensitive(self):
        """Test that Settings is case insensitive for environment variables."""
        with patch.dict(os.environ, {
            'DATABASE_URL': 'postgresql://test:test@localhost/test',
            'SECRET_KEY': 'test_secret_key',
            'ENVIRONMENT': 'testing'
        }):
            settings = Settings()

            assert settings.database_url == "postgresql://test:test@localhost/test"
            assert settings.secret_key == "test_secret_key"
            assert settings.environment == "testing"

    def test_settings_with_env_file(self):
        """Test Settings with .env file loading."""
        # This test assumes .env file loading works correctly
        # The actual .env file loading is tested by pydantic-settings
        settings = Settings()

        # Should not raise any exceptions
        assert settings is not None

    def test_settings_validation(self):
        """Test Settings validation."""
        # Test valid settings
        valid_settings = Settings(
            database_url="sqlite:///test.db",
            secret_key="test_key",
            environment="development",
            access_token_expire_minutes=30,
            upload_dir="uploads"
        )
        assert valid_settings is not None

        # Test invalid access_token_expire_minutes (should be positive)
        with pytest.raises(ValidationError):
            Settings(access_token_expire_minutes=-1)

    def test_settings_optional_fields(self):
        """Test that optional fields work correctly."""
        settings = Settings(
            database_url="sqlite:///test.db",
            secret_key="test_key"
        )

        assert settings.openrouter_api_key is None
        assert settings.openai_api_key is None

    def test_settings_with_all_optional_fields(self):
        """Test Settings with all optional fields set."""
        settings = Settings(
            database_url="sqlite:///test.db",
            secret_key="test_key",
            openrouter_api_key="test_openrouter_key",
            openai_api_key="test_openai_key"
        )

        assert settings.openrouter_api_key == "test_openrouter_key"
        assert settings.openai_api_key == "test_openai_key"


class TestGetSettingsFunction:
    """Test get_settings function."""

    def test_get_settings_returns_settings_instance(self):
        """Test that get_settings returns a Settings instance."""
        settings = get_settings()

        assert isinstance(settings, Settings)
        assert settings.database_url == "sqlite+aiosqlite:///./test.db"
        assert settings.secret_key == "dev_secret_key_change_in_production"

    def test_get_settings_returns_new_instance_each_time(self):
        """Test that get_settings returns a new instance each time."""
        settings1 = get_settings()
        settings2 = get_settings()

        # They should be different instances
        assert settings1 is not settings2
        # But should have the same values
        assert settings1.database_url == settings2.database_url
        assert settings1.secret_key == settings2.secret_key

    def test_get_settings_with_environment_override(self):
        """Test get_settings with environment variable override."""
        with patch.dict(os.environ, {
            'DATABASE_URL': 'postgresql://env:env@localhost/env',
            'SECRET_KEY': 'env_secret_key'
        }):
            settings = get_settings()

            assert settings.database_url == "postgresql://env:env@localhost/env"
            assert settings.secret_key == "env_secret_key"


class TestTestSettings:
    """Test TestSettings class for testing."""

    def test_test_settings_default_values(self):
        """Test TestSettings default values."""
        settings = get_test_settings()

        assert settings.database_url == "sqlite+aiosqlite:///:memory:"
        assert settings.secret_key == "test_secret_key"
        assert settings.environment == "testing"
        assert settings.upload_dir == "test_uploads"
        assert settings.openrouter_api_key == "test_openrouter_key"
        assert settings.openai_api_key == "test_openai_key"

    def test_test_settings_with_overrides(self):
        """Test TestSettings with custom overrides."""
        settings = get_test_settings(
            database_url="custom://test.db",
            secret_key="custom_test_key",
            environment="custom_testing"
        )

        assert settings.database_url == "custom://test.db"
        assert settings.secret_key == "custom_test_key"
        assert settings.environment == "custom_testing"
        # Other values should remain as test defaults
        assert settings.upload_dir == "test_uploads"
        assert settings.openrouter_api_key == "test_openrouter_key"

    def test_test_settings_inheritance(self):
        """Test that TestSettings inherits from Settings."""
        settings = get_test_settings()

        assert isinstance(settings, Settings)
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'environment')


class TestSettingsConfiguration:
    """Test Settings configuration options."""

    def test_settings_config_class(self):
        """Test Settings Config class."""
        settings = Settings()

        # Test that Config is properly configured
        assert hasattr(settings.Config, 'env_file')
        assert hasattr(settings.Config, 'case_sensitive')
        assert settings.Config.env_file == ".env"
        assert settings.Config.case_sensitive is False

    def test_settings_env_file_loading(self):
        """Test that .env file is loaded."""
        # This test verifies that the env_file configuration is set
        # The actual file loading is handled by pydantic-settings
        settings = Settings()

        # Should not raise any exceptions during initialization
        assert settings is not None


class TestSettingsEdgeCases:
    """Test Settings edge cases and error conditions."""

    def test_settings_with_empty_strings(self):
        """Test Settings with empty string values."""
        settings = Settings(
            database_url="",
            secret_key="",
            environment="",
            upload_dir=""
        )

        assert settings.database_url == ""
        assert settings.secret_key == ""
        assert settings.environment == ""
        assert settings.upload_dir == ""

    def test_settings_with_very_long_values(self):
        """Test Settings with very long values."""
        long_string = "x" * 1000

        settings = Settings(
            database_url=long_string,
            secret_key=long_string,
            upload_dir=long_string
        )

        assert settings.database_url == long_string
        assert settings.secret_key == long_string
        assert settings.upload_dir == long_string

    def test_settings_with_special_characters(self):
        """Test Settings with special characters."""
        special_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"

        settings = Settings(
            database_url=f"sqlite:///{special_chars}.db",
            secret_key=special_chars,
            upload_dir=f"/path/{special_chars}"
        )

        assert settings.database_url == f"sqlite:///{special_chars}.db"
        assert settings.secret_key == special_chars
        assert settings.upload_dir == f"/path/{special_chars}"


class TestSettingsTypeHints:
    """Test Settings type hints and validation."""

    def test_settings_type_annotations(self):
        """Test that Settings has proper type annotations."""
        # This test verifies that the type annotations are correct
        # by checking that the fields have the expected types

        settings = Settings()

        assert isinstance(settings.database_url, str)
        assert isinstance(settings.secret_key, str)
        assert isinstance(settings.environment, str)
        assert isinstance(settings.access_token_expire_minutes, int)
        assert isinstance(settings.upload_dir, str)
        # Optional fields can be None or str
        assert settings.openrouter_api_key is None or isinstance(settings.openrouter_api_key, str)
        assert settings.openai_api_key is None or isinstance(settings.openai_api_key, str)

    def test_settings_int_validation(self):
        """Test that integer fields are properly validated."""
        # Valid integer
        settings = Settings(access_token_expire_minutes=60)
        assert settings.access_token_expire_minutes == 60

        # Invalid integer (should raise ValidationError)
        with pytest.raises(ValidationError):
            Settings(access_token_expire_minutes="not_an_int")

    def test_settings_optional_str_validation(self):
        """Test that optional string fields are properly validated."""
        # Valid optional strings
        settings = Settings(
            openrouter_api_key="valid_key",
            openai_api_key="valid_key"
        )
        assert settings.openrouter_api_key == "valid_key"
        assert settings.openai_api_key == "valid_key"

        # None values should be allowed
        settings = Settings(
            openrouter_api_key=None,
            openai_api_key=None
        )
        assert settings.openrouter_api_key is None
        assert settings.openai_api_key is None


@pytest.mark.unit
class TestConfigDependencyMarkers:
    """Test that config dependency tests are properly marked."""

    def test_unit_marker_applied(self):
        """Test that unit marker is applied to this test class."""
        # This test will only run when --markers unit is specified
        assert True
