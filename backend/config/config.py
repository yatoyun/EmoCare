import os

STAGE = os.getenv("STAGE")
SECRET_KEY = os.getenv("SECRET_KEY")

class _Config:
    def __init__(self):
        self.STAGE = STAGE
        self.SECRET_KEY = SECRET_KEY
        if STAGE == "local":
            self.DEBUG = True
            local_host = "http://localhost:5173"
            self.ALLOWED_HOSTS = ["localhost","127.0.0.1"]
            self.CORS_ALLOWED_ORIGINS = [local_host]
            self.CORS_ORIGIN_WHITELIST = [local_host]
            self.CSRF_TRUSTED_ORIGINS = [local_host]
        else:
            # production
            self.DEBUG = False
            client_host = os.getenv("CLIENT_HOST")
            self.ALLOWED_HOSTS = [client_host.split("//")[1]]
            self.CORS_ALLOWED_ORIGINS = [client_host]
            self.CORS_ORIGIN_WHITELIST = [client_host]
            self.CSRF_TRUSTED_ORIGINS = [client_host]

config = _Config()