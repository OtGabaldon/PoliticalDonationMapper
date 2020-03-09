import pytest
from unittest.mock import Mock, patch

from opensecrets.client import OpenSecretsClient
from tests.mock_response.get_legislator_FL import get_legislator_FL

@patch('opensecrets.client.requests.get')
def test_open_secrets_success(mock_get):
    mock_get.return_value = Mock(status = 200)
    mock_get.return_value.json.return_value = get_legislator_FL
    client = OpenSecretsClient()
    legislators = client.call_open_secrets('get_legislators', ['FL'])
    assert (type({}) == type(legislators))

@patch('opensecrets.client.requests.get')
def test_open_secrets_error(mock_get):
    mock_get.return_value = Mock(status_code = 404)
    client = OpenSecretsClient()
    legislators = client.call_open_secrets('get_legislators', ['FL'])
    print (legislators)
    assert (legislators['err'] ==
           'Request for {} with paramaters: {} errord with {}'
           .format('get_legislators', ['FL'], '404') )

@patch('opensecrets.client.OpenSecretsClient.call_open_secrets')
def test_get_legislators_FL(mock_call_open_secrets):
    mock_call_open_secrets.return_value = get_legislator_FL
    client = OpenSecretsClient()
    response = client.get_legislators('FL')
    assert(response == client.legislators['FL'])

    legislator_name = list(response.keys())[0]
    assert (response[legislator_name]['firstlast'] == legislator_name)

