"""
Property model for the property listings application.
"""
from django.db import models


class Property(models.Model):
    """Model representing a property listing."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta options for Property model."""
        verbose_name_plural = 'Properties'
        ordering = ['-created_at']

    def __str__(self) -> str:
        """Return string representation of Property."""
        return f"{self.title} - {self.location}"
