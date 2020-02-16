from wrapper.OpenSecretsClient import OpenSecretsClient
from requests import codes

def test_get_legislators():
    client = OpenSecretsClient()
    response = client.get_legislators('FL')
    assert (codes.ok == response.status_code)
    assert (type([]) == type(response.json()['response']['legislator']))