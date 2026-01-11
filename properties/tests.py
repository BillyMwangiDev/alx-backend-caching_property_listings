"""
Tests for properties app.
"""
import pytest
from django.test import TestCase, Client
from django.core.cache import cache
from decimal import Decimal
from .models import Property
from .utils import getallproperties, getrediscachemetrics


class PropertyModelTest(TestCase):
    """Test cases for Property model."""

    def setUp(self):
        """Set up test data."""
        self.property = Property.objects.create(
            title='Test Property',
            description='A test property description',
            price=Decimal('100000.00'),
            location='Test City',
        )

    def test_property_creation(self):
        """Test that a property can be created."""
        self.assertEqual(self.property.title, 'Test Property')
        self.assertEqual(self.property.location, 'Test City')
        self.assertEqual(self.property.price, Decimal('100000.00'))
        self.assertIsNotNone(self.property.created_at)

    def test_property_str_representation(self):
        """Test string representation of Property."""
        expected = f"{self.property.title} - {self.property.location}"
        self.assertEqual(str(self.property), expected)


class PropertyListViewTest(TestCase):
    """Test cases for property list view."""

    def setUp(self):
        """Set up test data."""
        self.client = Client()
        cache.clear()  # Clear cache before each test
        Property.objects.create(
            title='Property 1',
            description='Description 1',
            price=Decimal('100000.00'),
            location='City 1',
        )
        Property.objects.create(
            title='Property 2',
            description='Description 2',
            price=Decimal('200000.00'),
            location='City 2',
        )

    def test_property_list_view_returns_properties(self):
        """Test that property list view returns all properties."""
        response = self.client.get('/properties/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('properties', data)
        self.assertEqual(len(data['properties']), 2)

    def test_property_list_view_structure(self):
        """Test that property list view returns correct structure."""
        response = self.client.get('/properties/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        property_data = data['properties'][0]
        self.assertIn('id', property_data)
        self.assertIn('title', property_data)
        self.assertIn('description', property_data)
        self.assertIn('price', property_data)
        self.assertIn('location', property_data)
        self.assertIn('created_at', property_data)


class PropertyCacheTest(TestCase):
    """Test cases for property caching functionality."""

    def setUp(self):
        """Set up test data."""
        cache.clear()
        Property.objects.create(
            title='Cached Property',
            description='A property for cache testing',
            price=Decimal('150000.00'),
            location='Cache City',
        )

    def test_get_all_properties_caches_result(self):
        """Test that getallproperties caches the result."""
        # First call should fetch from database
        properties1 = getallproperties()
        self.assertEqual(len(properties1), 1)

        # Second call should use cache
        properties2 = getallproperties()
        self.assertEqual(len(properties2), 1)
        self.assertEqual(properties1[0].id, properties2[0].id)

    def test_cache_invalidation_on_save(self):
        """Test that cache is invalidated when a property is saved."""
        # Populate cache
        getallproperties()
        self.assertIsNotNone(cache.get('allproperties'))

        # Create a new property (should trigger signal)
        Property.objects.create(
            title='New Property',
            description='New description',
            price=Decimal('200000.00'),
            location='New City',
        )

        # Cache should be invalidated
        self.assertIsNone(cache.get('allproperties'))

    def test_cache_invalidation_on_delete(self):
        """Test that cache is invalidated when a property is deleted."""
        property_obj = Property.objects.first()
        # Populate cache
        getallproperties()
        self.assertIsNotNone(cache.get('allproperties'))

        # Delete property (should trigger signal)
        property_obj.delete()

        # Cache should be invalidated
        self.assertIsNone(cache.get('allproperties'))


class CacheMetricsTest(TestCase):
    """Test cases for cache metrics functionality."""

    def setUp(self):
        """Set up test data."""
        cache.clear()

    def test_get_redis_cache_metrics_returns_dict(self):
        """Test that getrediscachemetrics returns a dictionary."""
        metrics = getrediscachemetrics()
        self.assertIsInstance(metrics, dict)
        self.assertIn('hits', metrics)
        self.assertIn('misses', metrics)
        self.assertIn('hit_ratio', metrics)
        self.assertIn('total_requests', metrics)

    def test_cache_metrics_structure(self):
        """Test that cache metrics have correct structure."""
        metrics = getrediscachemetrics()
        self.assertIsInstance(metrics['hits'], int)
        self.assertIsInstance(metrics['misses'], int)
        self.assertIsInstance(metrics['hit_ratio'], float)
        self.assertIsInstance(metrics['total_requests'], int)
        self.assertGreaterEqual(metrics['hit_ratio'], 0.0)
        self.assertLessEqual(metrics['hit_ratio'], 1.0)
