import pytest, json
from api.models import Quote
from rest_framework import status
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_random_quote_view_returns_random_quote():
    Quote.objects.create(quote_text="Quote 1", author="Author 1", likes=5)
    Quote.objects.create(quote_text="Quote 2", author="Author 2", likes=3)

    client = APIClient()
    response = client.post("/api/v1/quote",
                           data=json.dumps([]),  # Convert the list to a JSON string
                           content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    assert "quoteText" in response.data
    assert "author" in response.data


@pytest.mark.django_db
def test_random_quote_view_excludes_quotes_in_ids_to_exclude():
    quotes = []
    for nr in range(0, 20):
        quotes.append(create_quote(nr))

    # Exclude all but last
    excludeList = []
    for nr in range (0,19):
        excludeList.append(quotes[nr].id)

    print(excludeList)

    client = APIClient()
    response = client.post("/api/v1/quote",
                           data=json.dumps(excludeList),
                           content_type="application/json")

    print(f'response.data={response.data}')

    assert response.status_code == status.HTTP_200_OK
    assert response.data.get("quoteText") == 'Quote19'


@pytest.mark.django_db
def test_random_quote_view_returns_error_if_ids_not_list():
    client = APIClient()
    response = client.post("/api/v1/quote", {"ids": "not_a_list"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data == {"error": "The 'ids' field must be a list."}


@pytest.mark.django_db
def test_random_quote_view_fetches_quotes_from_api_when_less_than_10_in_db(mocker):
    mock_fetch_method = mocker.patch('api.views.random_quote_view.RandomQuoteView.fetch_and_add_zenquotes_to_db')
    create_quote(1)

    client = APIClient()
    response = client.post("/api/v1/quote",
                           data=json.dumps([]),
                           content_type="application/json")

    assert response.status_code == status.HTTP_200_OK
    mock_fetch_method.assert_called_once()


@pytest.mark.django_db
def test_random_quote_view_fetches_quotes_if_all_excluded(mocker):
    mock_fetch_method = mocker.patch("api.views.random_quote_view.RandomQuoteView.fetch_and_add_zenquotes_to_db")
    quotes = []
    for nr in range(0, 20):
        quotes.append(create_quote(nr))

    # Exclude all but last
    excludeList = []
    for nr in range (0,20):
        excludeList.append(quotes[nr].id)

    client = APIClient()
    response = client.post("/api/v1/quote",
                           data=json.dumps(excludeList),
                           content_type="application/json")
    #response = client.post("/api/v1/quote", [quote1.id])

    # fetch_and_add_zenquotes is mocked, so no extra quotes are fetched, which results in a 404
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data == {"message": "No quotes are available."}
    mock_fetch_method.assert_called_once()

def create_quote(nr):
    return Quote.objects.create(quote_text=f'Quote{nr}', author=f'Author{nr}', likes=0)
