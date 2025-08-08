from enum import Enum


class JWTTokenType(Enum):
    ACCESS_TOKEN = "Access Token"
    REFRESH_TOKEN = "Refresh Token"


class JWTTokenKey(Enum):
    ID = 'id'
    EXPIRY = 'expiry'
    TOKEN_TYPE = 'token_type'
    IS_GUEST = 'is_guest'


class Algorithm(Enum):
    HS256 = 'HS256'