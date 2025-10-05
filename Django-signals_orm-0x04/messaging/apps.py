from django.apps import AppConfig


class MessagingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "messaging"

    def ready(self):
        # Import signal handlers to ensure they're connected
        from . import signals  # noqa: F401
        # Reference the module to avoid "imported but unused" warnings
        try:
            from . import signals  # noqa: F401
        except ImportError:
            # No signals module present; nothing to connect
            signals = None
        else:
            # Reference the module to avoid "imported but unused" warnings
            _ = signals
