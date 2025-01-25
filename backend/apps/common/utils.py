import os
import logging
from typing import Dict, Optional
import boto3
import json
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

# AWS関連の設定
AWS_CONFIG = {
    "REGION": os.getenv("AWS_REGION", "ap-northeast-1"),
    "SECRET_NAME": os.getenv("AWS_SECRET_NAME"),
    "STAGE": os.getenv("STAGE", "production"),
    "LOCALSTACK_URL": "http://localstack:4566"
}

def _create_secrets_client() -> boto3.client:
    """SecretsManagerのクライアントを作成します。"""
    if AWS_CONFIG["STAGE"] == "local":
        return boto3.client(
            "secretsmanager",
            region_name=AWS_CONFIG["REGION"],
            endpoint_url=AWS_CONFIG["LOCALSTACK_URL"],
            aws_access_key_id="dummy",
            aws_secret_access_key="dummy"
        )
    return boto3.client("secretsmanager", region_name=AWS_CONFIG["REGION"])

def get_secret_values() -> Dict[str, str]:
    """シークレットマネージャーから全ての秘密情報を取得します。

    Returns:
        Dict[str, str]: シークレット情報の辞書

    Raises:
        ValueError: 環境変数が未設定の場合
        ClientError: AWS API呼び出しエラーの場合
    """
    if not AWS_CONFIG["SECRET_NAME"]:
        raise ValueError("AWS_SECRET_NAME environment variable is not set")

    try:
        client = _create_secrets_client()
        response = client.get_secret_value(SecretId=AWS_CONFIG["SECRET_NAME"])
    except ClientError as e:
        logger.error(
            f"Failed to retrieve secret '{AWS_CONFIG['SECRET_NAME']}'. "
            f"Error code: {e.response.get('Error', {}).get('Code', 'Unknown')}"
        )
        raise

    if "SecretString" not in response:
        raise ValueError(f"Secret '{AWS_CONFIG['SECRET_NAME']}' does not contain a string value")

    return json.loads(response["SecretString"])

def get_secret_value(key: str) -> str:
    """特定のキーの秘密情報を取得します。

    Args:
        key: 取得するシークレットのキー

    Returns:
        str: シークレット値

    Raises:
        ValueError: キーが無効な場合
    """
    if not key:
        raise ValueError("Key parameter cannot be empty")

    secret_dict = get_secret_values()
    
    if key not in secret_dict:
        raise ValueError(f"Key '{key}' not found in secret '{AWS_CONFIG['SECRET_NAME']}'")

    return secret_dict[key]