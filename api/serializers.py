from rest_framework import serializers
from .models import Quote

class QuoteSerializer(serializers.ModelSerializer):
    # quote_text in the model should be mapped to quoteText in the json
    quoteText = serializers.CharField(source='quote_text')

    class Meta:
        model = Quote
        fields = ['id', 'author', 'quoteText', 'likes']
