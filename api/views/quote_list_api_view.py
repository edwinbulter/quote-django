from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Quote
from ..serializers import QuoteSerializer

class QuoteListAPIView(APIView):
    def get(self, request):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)