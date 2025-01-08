import logging
import random

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Quote
from ..serializers import QuoteSerializer

logger = logging.getLogger(__name__)

class RandomQuoteView(APIView):
    def get(self, request, *args, **kwargs):
        request._full_data = []
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        ids_to_exclude = request.data
        logging.info(f"Fetch a random Quote, skipping ids {ids_to_exclude}")

        if not isinstance(ids_to_exclude, list):
            return Response({"error": "The 'ids' field must be a list."},
                            status=status.HTTP_400_BAD_REQUEST)

        logging.info(f'Number of quotes in the database: {Quote.objects.count()}')

        if (Quote.objects.count() < 10):
            logging.info(f'Start fetching quotes from ZEN because the database contains only {Quote.objects.count()} quotes')
            self.fetch_and_add_zenquotes_to_db()
            logging.info(f'Number of quotes in the database after adding quotes from ZenQuotes API: {Quote.objects.count()}')

        remaining_quotes = Quote.objects.exclude(id__in=ids_to_exclude)

        if (len(remaining_quotes) < 1):
            logging.info(f'Start fetching quotes almost all database quotes ({Quote.objects.count()}) are excluded {len(ids_to_exclude)}')
            self.fetch_and_add_zenquotes_to_db()
            remaining_quotes = Quote.objects.exclude(id__in=ids_to_exclude)
            logging.info(f'Number of quotes in the database after adding quotes from ZenQuotes API: {Quote.objects.count()}')

        if not remaining_quotes.exists():
            return Response({"message": "No quotes are available."},
                            status=status.HTTP_404_NOT_FOUND)

        random_quote = random.choice(remaining_quotes)

        serializer = QuoteSerializer(random_quote)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def fetch_and_add_zenquotes_to_db(self):
        # URL of the ZenQuotes API
        url = 'https://zenquotes.io/api/quotes'

        try:
            response = requests.get(url)
            response.raise_for_status()  # throw Exception for HTTP request errors

            quotes = response.json()

            saved_quotes = []
            for quote_data in quotes:
                zen_quote_text = quote_data.get('q')  # Quote text field from the API
                zen_author = quote_data.get('a')  # Author field from the API

                # Ensure no duplicate quote is added to the database
                if not Quote.objects.filter(quote_text=zen_quote_text, author=zen_author).exists():
                    quote = Quote.objects.create(quote_text=zen_quote_text, author=zen_author, likes=0)
                    saved_quotes.append(quote)

        except requests.RequestException as e:
            logging.error("Failed to fetch data from ZenQuotes API: %s", e, exc_info=True)
        except Exception as e:
            logging.error("An unexpected error occurred.", e, exc_info=True)
