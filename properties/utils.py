"""
Utility functions for properties app.
"""

import logging
from typing import List, Dict, Any
from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property

logger = logging.getLogger(__name__)


def getallproperties() -> List[Property]:
    """
    Get all properties with low-level caching.

    Checks Redis for cached queryset. If not found, fetches from database
    and stores in Redis for 1 hour (3600 seconds).

    Returns:
        List[Property]: QuerySet of all properties
    """
    cache_key = "allproperties"
    cached_properties = cache.get(cache_key)

    if cached_properties is not None:
        logger.debug("Cache hit for allproperties")
        return cached_properties

    logger.debug("Cache miss for allproperties, fetching from database")
    properties = list(Property.objects.all())
    cache.set(cache_key, properties, 3600)  # Cache for 1 hour
    logger.info(f"Cached {len(properties)} properties for 1 hour")
    return properties


def getall_properties() -> List[Property]:
    """Alias for getallproperties() to match view requirements."""
    return getallproperties()


def getrediscachemetrics() -> Dict[str, Any]:
    """
    Retrieve and analyze Redis cache hit/miss metrics.

    Connects to Redis via django_redis, retrieves keyspace_hits and
    keyspace_misses from INFO command, and calculates hit ratio.

    Returns:
        Dict containing:
            - hits: Number of cache hits
            - misses: Number of cache misses
            - hit_ratio: Calculated hit ratio (hits / (hits + misses))
            - total_requests: Total cache requests
    """
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses

        hit_ratio = 0.0
        if total_requests > 0:
            hit_ratio = hits / total_requests

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": round(hit_ratio, 4),
            "total_requests": total_requests,
        }

        logger.info(
            f"Cache metrics - Hits: {hits}, Misses: {misses}, "
            f"Hit Ratio: {hit_ratio:.2%}"
        )

        return metrics

    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}", exc_info=True)
        return {
            "hits": 0,
            "misses": 0,
            "hit_ratio": 0.0,
            "total_requests": 0,
            "error": str(e),
        }
