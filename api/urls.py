from django.urls import path

from .views.liked_quote_list_api_view import LikedQuoteListAPIView
from .views.quote_detail_api_view import QuoteDetailAPIView
from .views.quote_like_api_view import QuoteLikeAPIView
from .views.quote_list_api_view import QuoteListAPIView
from .views.random_quote_view import RandomQuoteView

urlpatterns = [
    # Retrieve all quotes
    path('quotes', QuoteListAPIView.as_view(), name='quotes'),

    # Retrieve all liked quotes
    path('quote/liked', LikedQuoteListAPIView.as_view(), name='liked-quotes'),

    # Retrieve a single quote by its id
    path('quote/<int:pk>', QuoteDetailAPIView.as_view(), name='quote-detail'),

    # Like a specific quote
    path('quote/<int:pk>/like', QuoteLikeAPIView.as_view(), name='like'),

    # Retrieve a random quote by get or by post with a list of ids to exclude in the body
    path('quote', RandomQuoteView.as_view(), name='quote'),
]