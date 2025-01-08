# tests/test_liked_quote_list_api_view.py

import pytest
from api.models import Quote
from api.serializers import QuoteSerializer
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_get_liked_quotes_returns_only_liked_quotes():
    # Arrange
    Quote.objects.create(quote_text="Quote 1", author='Author 1', likes=5)
    Quote.objects.create(quote_text="Quote 2", author='Author 2', likes=0)

    client = APIClient()

    # Act
    response = client.get("/api/v1/quote/liked")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    expected_data = QuoteSerializer(Quote.objects.filter(likes__gt=0).order_by("-likes"), many=True).data
    assert response.json() == expected_data


@pytest.mark.django_db
def test_get_liked_quotes_returns_empty_list_if_no_liked_quotes():
    # Arrange
    Quote.objects.create(quote_text="Quote 1", author='Author 1', likes=0)
    Quote.objects.create(quote_text="Quote 2", author='Author 2', likes=0)

    client = APIClient()

    # Act
    response = client.get("/api/v1/quote/liked")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


@pytest.mark.django_db
def test_get_liked_quotes_orders_by_likes_descending():
    # Arrange
    Quote.objects.create(quote_text="Quote 1", author='Author 1', likes=1)
    Quote.objects.create(quote_text="Quote 2", author='Author 2', likes=10)
    Quote.objects.create(quote_text="Quote 3", author='Author 3', likes=7)

    client = APIClient()

    # Act
    response = client.get("/api/v1/quote/liked")

    # Assert
    assert response.status_code == status.HTTP_200_OK
    liked_quotes = Quote.objects.filter(likes__gt=0).order_by("-likes")
    expected_data = QuoteSerializer(liked_quotes, many=True).data
    assert response.json() == expected_data
