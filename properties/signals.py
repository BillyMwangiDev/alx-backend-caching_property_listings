"""
Signal handlers for properties app.
"""
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Property)
def invalidate_cache_on_save(sender, instance, **kwargs):
    """
    Invalidate all_properties cache when a Property is created or updated.

    Args:
        sender: The model class (Property)
        instance: The instance being saved
        **kwargs: Additional keyword arguments
    """
    cache_key = 'allproperties'
    cache.delete(cache_key)
    logger.info(f"Cache invalidated for {cache_key} after save of Property {instance.id}")


@receiver(post_delete, sender=Property)
def invalidate_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate all_properties cache when a Property is deleted.

    Args:
        sender: The model class (Property)
        instance: The instance being deleted
        **kwargs: Additional keyword arguments
    """
    cache_key = 'allproperties'
    cache.delete(cache_key)
    logger.info(f"Cache invalidated for {cache_key} after delete of Property {instance.id}")
