import os
import unittest
from unittest.mock import patch

from governance_platform.config import load_settings


class LoadSettingsTest(unittest.TestCase):
    def test_loads_default_settings(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            settings = load_settings()

        self.assertEqual(
            settings.project_name,
            "enterprise-ai-data-governance-platform",
        )
        self.assertEqual(settings.app_env, "local")
        self.assertEqual(settings.postgres_port, 5432)
        self.assertEqual(settings.qdrant_port, 6333)

    def test_loads_environment_overrides(self) -> None:
        env = {
            "PROJECT_NAME": "test-platform",
            "APP_ENV": "test",
            "POSTGRES_PORT": "15432",
            "QDRANT_PORT": "16333",
        }

        with patch.dict(os.environ, env, clear=True):
            settings = load_settings()

        self.assertEqual(settings.project_name, "test-platform")
        self.assertEqual(settings.app_env, "test")
        self.assertEqual(settings.postgres_port, 15432)
        self.assertEqual(settings.qdrant_port, 16333)

    def test_invalid_integer_setting_raises_error(self) -> None:
        with patch.dict(os.environ, {"POSTGRES_PORT": "not-a-port"}, clear=True):
            with self.assertRaises(ValueError):
                load_settings()


if __name__ == "__main__":
    unittest.main()

