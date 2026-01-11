"""
Django app configuration for properties app.
"""
from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    """Configuration for properties app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self) -> None:
        """Import signals when app is ready."""
        import properties.signals  # noqa: F401
