import os
from logging import getLogger

STAGE = os.getenv("STAGE")
SECRET_KEY = os.getenv("SECRET_KEY")
AWS_REGION = os.getenv("AWS_REGION")
client_hosts = os.getenv("CLIENT_HOST").split(",")

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