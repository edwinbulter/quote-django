from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Quote
from ..serializers import QuoteSerializer

class QuoteDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        quote = self.get_object(pk)
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)
