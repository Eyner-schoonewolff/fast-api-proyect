import fastapi_jwt
from datetime import timedelta


class JwtConfig:
    def __init__(self):
        self.access_security = fastapi_jwt.JwtAccessBearer(
            secret_key="HASH-2000-23",
            auto_error=True,
            access_expires_delta=timedelta(days=1),
        )

    def get_access_security(self):
        return self.access_security


jwt_config = JwtConfig()
