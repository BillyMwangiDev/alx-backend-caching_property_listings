# Usage Guide - Property Listings Caching

## Overview

This guide explains how to use the caching features implemented in the property listings application.

## Caching Layers

The application implements two caching layers:

1. **View-level caching** (15 minutes): Caches the entire HTTP response
2. **Low-level caching** (1 hour): Caches the Property queryset in Redis

## API Usage

### Get All Properties

```bash
# First request - cache miss, fetches from database
curl http://localhost:8000/properties/

# Subsequent requests within 15 minutes - served from cache
curl http://localhost:8000/properties/
```

### Response Format

```json
{
  "properties": [
    {
      "id": 1,
      "title": "Beautiful House",
      "description": "A beautiful house in the city",
      "price": "250000.00",
      "location": "New York",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

## Programmatic Usage

### Using get_all_properties()

```python
from properties.utils import get_all_properties

# This function automatically handles caching
properties = get_all_properties()
for prop in properties:
    print(f"{prop.title} - {prop.location}")
```

### Getting Cache Metrics

```python
from properties.utils import get_redis_cache_metrics

metrics = get_redis_cache_metrics()
print(f"Cache Hits: {metrics['hits']}")
print(f"Cache Misses: {metrics['misses']}")
print(f"Hit Ratio: {metrics['hit_ratio']:.2%}")
print(f"Total Requests: {metrics['total_requests']}")
```

## Cache Invalidation

Cache is automatically invalidated when:

1. A new property is created
2. An existing property is updated
3. A property is deleted

This happens via Django signals - no manual intervention needed.

### Manual Cache Invalidation

If needed, you can manually clear the cache:

```python
from django.core.cache import cache

# Clear specific key
cache.delete('all_properties')

# Clear all cache
cache.clear()
```

## Monitoring Cache Performance

### View Cache Metrics in Logs

The application logs cache operations:

```
INFO properties.utils: Cache miss for all_properties, fetching from database
INFO properties.utils: Cached 10 properties for 1 hour
INFO properties.utils: Cache metrics - Hits: 50, Misses: 10, Hit Ratio: 83.33%
```

### Check Redis Directly

```bash
# Connect to Redis
docker exec -it property_listings_redis redis-cli

# Check keys
KEYS *

# Get cache statistics
INFO stats
```

## Best Practices

1. **Monitor hit ratios**: Aim for >80% hit ratio for optimal performance
2. **Adjust TTL if needed**: If properties change frequently, reduce TTL
3. **Use signals**: Always use signals for cache invalidation, not manual clearing
4. **Test cache behavior**: Verify cache invalidation works correctly in tests

## Troubleshooting

### Cache Not Working

1. Check Redis is running: `docker-compose ps`
2. Verify Redis connection in settings
3. Check logs for connection errors

### Stale Data

1. Verify signals are registered (check `properties/apps.py`)
2. Check signal handlers are firing (check logs)
3. Manually clear cache if needed

### Low Hit Ratio

1. Check if TTL is too short
2. Verify cache is being used (check logs)
3. Consider increasing TTL if data doesn't change often
