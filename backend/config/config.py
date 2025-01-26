import os
from logging import getLogger
from typing import List

logger = getLogger(__name__)

def get_env_variable(name: str, default: str = None) -> str:
    value = os.getenv(name)
    if value is None:
        if default is None:
            raise ValueError(f"The environment variable {name} is not set.")
        return default
    return value

STAGE = get_env_variable("STAGE", "development")
SECRET_KEY = get_env_variable("SECRET_KEY")
AWS_REGION = get_env_variable("AWS_REGION", "ap-northeast-1")
# DB settings
DB_NAME = get_env_variable("DB_NAME")
DB_HOST = get_env_variable("DB_HOST")
DB_USER = get_env_variable("DB_USER")
DB_PASS = get_env_variable("DB_PASS")


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
        self.DB_NAME = DB_NAME
        self.DB_HOST = DB_HOST
        self.DB_USER = DB_USER
        self.DB_PASS = DB_PASS

        if STAGE == "local":
            self.DEBUG = True
        else:
            # production
            self.DEBUG = False

def _get_domain(host: str) -> str:
    return host.split("//")[1].split(":")[0]

config = _Config()