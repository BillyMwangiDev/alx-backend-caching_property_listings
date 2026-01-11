# ALX Backend Caching - Property Listings

A Django application demonstrating Redis caching strategies for property listings, including view-level caching, low-level caching, cache invalidation, and cache metrics analysis.

## Features

- **Dockerized PostgreSQL and Redis**: Easy setup with Docker Compose
- **View-level Caching**: Property list view cached for 15 minutes using `@cache_page`
- **Low-level Caching**: Property queryset cached in Redis for 1 hour
- **Cache Invalidation**: Automatic cache invalidation on Property create/update/delete using Django signals
- **Cache Metrics**: Redis cache hit/miss ratio analysis

## Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── __init__.py
│   ├── settings.py          # Django settings with PostgreSQL and Redis config
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── properties/
│   ├── __init__.py          # App config import
│   ├── apps.py              # App config with signal registration
│   ├── models.py            # Property model
│   ├── views.py             # Property list view with caching
│   ├── urls.py              # Property URLs
│   ├── utils.py             # Caching utilities and metrics
│   ├── signals.py           # Cache invalidation signals
│   ├── admin.py             # Admin interface
│   └── tests.py             # Test suite
├── docker-compose.yml       # PostgreSQL and Redis services
├── Dockerfile               # Django application container
├── requirements.txt         # Python dependencies
├── pytest.ini              # Pytest configuration
├── .flake8                 # Flake8 linting configuration
├── .env.example            # Environment variables template
└── README.md

```

## Setup

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd alx-backend-caching_property_listings
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Start Docker services**:
   ```bash
   docker-compose up -d
   ```

6. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

7. **Create superuser (optional)**:
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The application will be available at `http://localhost:8000`

## Usage

### API Endpoints

- **GET /properties/**: Returns all properties (cached for 15 minutes)
  ```bash
   curl http://localhost:8000/properties/
   ```

### Admin Interface

Access the Django admin at `http://localhost:8000/admin/` to manage properties.

### Cache Metrics

To retrieve cache metrics programmatically:

```python
from properties.utils import get_redis_cache_metrics

metrics = get_redis_cache_metrics()
print(f"Hit Ratio: {metrics['hit_ratio']:.2%}")
```

## Implementation Details

### 1. View-level Caching

The `property_list` view uses Django's `@cache_page` decorator to cache the entire HTTP response for 15 minutes:

```python
@cache_page(60 * 15)  # 15 minutes
def property_list(request):
    # ...
```

### 2. Low-level Caching

The `get_all_properties()` utility function implements low-level caching:

- Checks Redis for cached queryset
- Fetches from database if cache miss
- Stores in Redis for 1 hour (3600 seconds)
- Returns the queryset

### 3. Cache Invalidation

Django signals automatically invalidate the cache when properties are created, updated, or deleted:

- `post_save` signal: Invalidates cache on create/update
- `post_delete` signal: Invalidates cache on delete

### 4. Cache Metrics

The `get_redis_cache_metrics()` function:

- Connects to Redis via django_redis
- Retrieves `keyspace_hits` and `keyspace_misses` from Redis INFO
- Calculates hit ratio: `hits / (hits + misses)`
- Returns metrics dictionary with logging

## Testing

Run tests using pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=properties
```

Run specific test file:

```bash
pytest properties/tests.py
```

## Linting and Formatting

### Run flake8:
```bash
flake8 .
```

### Format code with black:
```bash
black .
```

### Check formatting:
```bash
black --check .
```

## Security

### Dependency Scanning

Run pip-audit to check for vulnerable dependencies:

```bash
pip install pip-audit
pip-audit --requirement requirements.txt
```

## Docker

### Development with Docker Compose

Start services:
```bash
docker-compose up -d
```

Stop services:
```bash
docker-compose down
```

View logs:
```bash
docker-compose logs -f
```

### Build and Run with Docker

```bash
docker build -t property-listings .
docker run -p 8000:8000 property-listings
```

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/ci.yml`) that:

- Runs linting (flake8, black)
- Runs tests with PostgreSQL and Redis services
- Performs security checks (pip-audit)

## Environment Variables

Required environment variables (see `.env.example`):

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: PostgreSQL username
- `DB_PASSWORD`: PostgreSQL password
- `DB_HOST`: PostgreSQL host
- `DB_PORT`: PostgreSQL port
- `REDIS_HOST`: Redis host
- `REDIS_PORT`: Redis port
- `REDIS_DB`: Redis database number

## Deployment

### Production Considerations

1. Set `DEBUG=False` in production
2. Use a strong `SECRET_KEY`
3. Configure proper `ALLOWED_HOSTS`
4. Use environment-specific database credentials
5. Set up proper logging and monitoring
6. Use HTTPS
7. Configure Redis persistence if needed
8. Set up database backups

### Health Checks

The Docker Compose configuration includes health checks for both PostgreSQL and Redis services.

## Contributing

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests and linting: `pytest && flake8 . && black --check .`
4. Commit with descriptive messages
5. Push to your branch: `git push origin feature/your-feature-name`
6. Create a pull request

## License

This project is part of the ALX Backend curriculum.

## Author

ALX Backend Student
