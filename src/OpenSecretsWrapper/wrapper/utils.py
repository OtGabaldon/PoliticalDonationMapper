import boto3
import json
from wrapper.constants import BASE_URL
def get_open_secrets_secret():
    secret_name = "openSecretKey"
    region_name = "us-east-1"

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    return json.loads(
            client.get_secret_value(
                SecretId=secret_name
            )['SecretString']
        )[secret_name]

def get_base_url():
    api_key = get_open_secrets_secret()
    return BASE_URL.format(api_key)+'{}'



