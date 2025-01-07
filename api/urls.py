from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, RandomQuoteView

# Create a router instance
router = DefaultRouter()

# Register the viewset with the router
router.register(r'quote', QuoteViewSet, basename='quote')

urlpatterns = [
    # Include all automatically generated routes from the router
    *router.urls,

    # Add an alias for /quotes to also fetch all quotes
    path('quotes', QuoteViewSet.as_view({'get': 'list'}), name='quote'),

    # Add the specific path for RandomQuoteView
    path('quote', RandomQuoteView.as_view(), name='quote'),
]