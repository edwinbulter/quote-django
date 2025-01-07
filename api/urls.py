from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import QuoteViewSet, RandomQuoteView

router = DefaultRouter()

urlpatterns = [
    path('quotes', QuoteViewSet.as_view({'get': 'list'}), name='quotes'),
    path('quote', RandomQuoteView.as_view(), name='quote'),
]
