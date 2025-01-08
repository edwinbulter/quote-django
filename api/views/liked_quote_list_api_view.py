from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Quote
from ..serializers import QuoteSerializer

class LikedQuoteListAPIView(APIView):
    def get(self, request):
        liked_quotes = Quote.objects.filter(likes__gt=0).order_by('-likes')
        serializer = QuoteSerializer(liked_quotes, many=True)
        return Response(serializer.data)