import os
import logging
import boto3
import json
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

STAGE = os.getenv("STAGE")
AWS_SECRET_NAME = os.getenv("AWS_SECRET_NAME")

def get_secret_values() -> dict:
    """
    Retrieve secrets from AWS Secrets Manager or LocalStack.
    If STAGE is 'local', use LocalStack, otherwise assume production environment.

    :return: Secret dictionary
    :raises Exception: Throws an exception if retrieval fails
    """

    # Check is local
    is_local = (STAGE == "local")

    if is_local:
        REGION = os.getenv("AWS_REGION")
        _client = boto3.client(
            "secretsmanager",
            region_name=REGION,
            endpoint_url="http://localstack:4566",
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy",
        )
    else:
        _client = boto3.client("secretsmanager")

    try:
        # Retrieve secret value from SecretsManager
        response = _client.get_secret_value(SecretId=AWS_SECRET_NAME)
    except ClientError as e:
        # Log error and convert to application-specific exception
        logger.exception(f"Failed to retrieve secret '{AWS_SECRET_NAME}': {e}")
        raise Exception(f"Unable to retrieve secret: {AWS_SECRET_NAME}") from e

    # Return secret string
    if "SecretString" in response:
        return json.loads(response["SecretString"])
    else:
        # If stored in a non-string format like SecretBinary,
        # implement decoding as needed
        raise Exception(f"Secret '{AWS_SECRET_NAME}' is not a string type.")

def get_secret_value(key: str) -> str:
    """
    Retrieve a specific key from a secret stored in AWS Secrets Manager or LocalStack.

    :param AWS_SECRET_NAME: Name of the secret to retrieve (SecretId)
    :param key: Key to retrieve from the secret
    :param AWS_SECRET_NAME: Region name (default: ap-northeast-1)
    :return: Secret value for the specified key
    :raises Exception: Throws an exception if retrieval fails
    """
    secret_dict = get_secret_values()

    if key in secret_dict:
        return secret_dict[key]
    else:
        raise Exception(f"Key '{key}' not found in secret '{AWS_SECRET_NAME}'.")