import os
from logging import getLogger
from typing import List

logger = getLogger(__name__)

def get_env_variable(name: str, default: str = None) -> str:
    value = os.getenv(name)
    if value is None:
        if default is None:
            raise ValueError(f"環境変数{name}が設定されていません")
        return default
    return value

STAGE = get_env_variable("STAGE", "development")
SECRET_KEY = get_env_variable("SECRET_KEY")
AWS_REGION = get_env_variable("AWS_REGION", "ap-northeast-1")

def get_client_hosts() -> List[str]:
    hosts = get_env_variable("CLIENT_HOST", "http://localhost:3000")
    try:
        return hosts.split(",")
    except Exception as e:
        logger.error(f"CLIENT_HOSTの解析に失敗: {repr(e)}")
        return ["http://localhost:3000"]

client_hosts = get_client_hosts()

class _Config:
    def __init__(self):
        self.STAGE = STAGE
        self.SECRET_KEY = SECRET_KEY
        self.ALLOWED_HOSTS = [_get_domain(host) for host in client_hosts]
        self.CORS_ALLOWED_ORIGINS = client_hosts
        self.CORS_ORIGIN_WHITELIST = client_hosts
        self.CSRF_TRUSTED_ORIGINS = client_hosts
        self.CORS_ALLOWED_ORIGIN_REGEXES = [fr"^https://.*\.{AWS_REGION}\.elb\.amazonaws\.com$"]

        if STAGE == "local":
            self.DEBUG = True
        else:
            # production
            self.DEBUG = False

def _get_domain(host: str) -> str:
    return host.split("//")[1].split(":")[0]

config = _Config()