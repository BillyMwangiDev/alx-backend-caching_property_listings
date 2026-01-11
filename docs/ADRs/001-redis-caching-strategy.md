# ADR 001: Redis Caching Strategy for Property Listings

## Status
Accepted

## Context
The property listings application needs to handle high traffic efficiently. Database queries for property listings can become a bottleneck as the number of properties and concurrent users increase. We need a caching strategy to:

1. Reduce database load
2. Improve response times
3. Handle traffic spikes gracefully
4. Maintain data consistency

## Decision
We will implement a multi-layered caching strategy using Redis:

1. **View-level caching**: Cache entire HTTP responses for 15 minutes using Django's `@cache_page` decorator
2. **Low-level caching**: Cache Property querysets in Redis for 1 hour using Django's cache API
3. **Cache invalidation**: Use Django signals to automatically invalidate cache on Property create/update/delete operations
4. **Cache metrics**: Monitor cache performance using Redis INFO command

## Rationale

### Why Redis?
- Fast in-memory data store
- Widely used and well-supported
- Django has excellent Redis integration via django-redis
- Supports various data structures and operations
- Can be used for both caching and session storage

### Why Multi-layered Caching?
- **View-level caching**: Simplest to implement, caches entire response including serialization
- **Low-level caching**: More granular control, can be reused across different views
- **Combined approach**: Provides redundancy and flexibility

### Why 15 minutes for view cache?
- Balance between freshness and performance
- Properties don't change frequently
- 15 minutes is acceptable for listing views

### Why 1 hour for queryset cache?
- Longer TTL reduces database load
- Signals ensure cache invalidation on changes
- Acceptable for read-heavy workloads

### Why Signal-based Invalidation?
- Automatic and reliable
- No manual cache management needed
- Ensures data consistency
- Follows Django best practices

## Consequences

### Positive
- Significant reduction in database queries
- Improved response times
- Better scalability
- Automatic cache management via signals

### Negative
- Additional infrastructure (Redis server)
- Slight complexity in deployment
- Memory usage for cached data
- Need to monitor cache hit rates

### Mitigation
- Use Docker Compose for easy local development
- Monitor cache metrics to optimize TTL values
- Set up Redis persistence if needed
- Document cache invalidation behavior

## Implementation Notes

1. Cache keys use descriptive names: `all_properties`
2. TTL values are configurable via constants
3. Logging added for cache operations and metrics
4. Error handling for Redis connection issues
5. Tests verify cache behavior and invalidation

## Alternatives Considered

1. **Database query optimization only**: Not sufficient for high traffic
2. **File-based caching**: Slower than Redis, not suitable for distributed systems
3. **Memcached**: Similar to Redis but less feature-rich
4. **Application-level caching only**: Less efficient than Redis

## References

- [Django Caching Framework](https://docs.djangoproject.com/en/4.2/topics/cache/)
- [django-redis Documentation](https://django-redis.readthedocs.io/)
- [Redis Documentation](https://redis.io/docs/)
