import os

STAGE = os.getenv("STAGE")
SECRET_KEY = os.getenv("SECRET_KEY")
client_host = os.getenv("CLIENT_HOST")

class _Config:
    def __init__(self):
        self.STAGE = STAGE
        self.SECRET_KEY = SECRET_KEY
        self.ALLOWED_HOSTS = [client_host.split("//")[1].split(":")[0]]
        self.CORS_ALLOWED_ORIGINS = [client_host]
        self.CORS_ORIGIN_WHITELIST = [client_host]
        self.CSRF_TRUSTED_ORIGINS = [client_host]
        if STAGE == "local":
            self.DEBUG = True
        else:
            # production
            self.DEBUG = False


config = _Config()