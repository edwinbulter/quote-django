from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Quote

class QuoteLikeAPIView(APIView):
    def get_object(self, pk):
        try:
            return Quote.objects.get(pk=pk)
        except Quote.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        quote = self.get_object(pk)
        quote.likes += 1  # Increment the likes or modify as you see fit
        quote.save()

        return Response(quote.likes, status=status.HTTP_200_OK)
