"""
Views for properties app.
"""
import logging
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import get_all_properties

logger = logging.getLogger(__name__)


@cache_page(60 * 15)  # Cache for 15 minutes
@require_http_methods(["GET"])
def property_list(request):
    """
    View to return all properties.

    This view is cached for 15 minutes using the @cache_page decorator.
    It also uses low-level caching via get_all_properties() utility function.

    Args:
        request: HTTP request object

    Returns:
        JsonResponse: JSON response containing list of properties
    """
    try:
        properties = get_all_properties()
        properties_data = [
            {
                'id': prop.id,
                'title': prop.title,
                'description': prop.description,
                'price': str(prop.price),
                'location': prop.location,
                'created_at': prop.created_at.isoformat(),
            }
            for prop in properties
        ]
        logger.info(f"Returned {len(properties_data)} properties")
        return JsonResponse({'properties': properties_data}, safe=False)
    except Exception as e:
        logger.error(f"Error fetching properties: {str(e)}", exc_info=True)
        return JsonResponse(
            {'error': 'Failed to fetch properties', 'message': str(e)},
            status=500
        )
