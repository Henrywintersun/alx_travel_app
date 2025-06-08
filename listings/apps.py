from django.apps import AppConfig


class ListingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'listings'
    verbose_name = 'Travel Listings'
    
    def ready(self):
        """
        Import signals when the app is ready
        """
        try:
            import listings.signals
        except ImportError:
            pass
