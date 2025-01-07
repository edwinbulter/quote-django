from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import Quote
from .serializers import QuoteSerializer
import random
import requests
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level, e.g., DEBUG, INFO, etc.
    format='%(asctime)s - %(levelname)s - %(message)s'  # Define the log message format
)

class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

class RandomQuoteView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the list of IDs that should be excluded
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


        # Query the quotes, excluding the given IDs
        remaining_quotes = Quote.objects.exclude(id__in=ids_to_exclude)

        if (remaining_quotes < 2):
            logging.info(f'Start fetching quotes almost all database quotes ({Quote.objects.count()}) are excluded {len(ids_to_exclude)}')
            self.fetch_and_add_zenquotes_to_db()
            remaining_quotes = Quote.objects.exclude(id__in=ids_to_exclude)
            logging.info(f'Number of quotes in the database after adding quotes from ZenQuotes API: {Quote.objects.count()}')

        # If there are no remaining quotes, return an appropriate message
        if not remaining_quotes.exists():
            return Response({"message": "No quotes are available."},
                            status=status.HTTP_404_NOT_FOUND)

        # Pick a random quote from the remaining ones
        random_quote = random.choice(remaining_quotes)

        # Serialize the random quote
        serializer = QuoteSerializer(random_quote)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def fetch_and_add_zenquotes_to_db(self):
        # URL of the ZenQuotes API
        url = 'https://zenquotes.io/api/quotes'

        try:
            # Fetch quotes from the API
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP request errors

            # Parse the JSON response
            quotes = response.json()

            # Save each quote into the database
            saved_quotes = []
            for quote_data in quotes:
                zen_quote_text = quote_data.get('q')  # Quote text field from the API
                zen_author = quote_data.get('a')  # Author field from the API

                # Ensure no duplicate quote is added to the database
                if not Quote.objects.filter(quote_text=zen_quote_text, author=zen_author).exists():
                    quote = Quote.objects.create(quote_text=zen_quote_text, author=zen_author, likes=0)
                    saved_quotes.append(quote)

        except requests.RequestException as e:
            # Handle any request errors with an appropriate HTTP error message
            logging.error("Failed to fetch data from ZenQuotes API: %s", e, exc_info=True)
        except Exception as e:
            logging.error("An unexpected error occurred.", e, exc_info=True)
