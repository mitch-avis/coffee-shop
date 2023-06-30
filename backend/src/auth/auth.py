"""
    auth.py
"""
import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

AUTH0_DOMAIN = "dev-5txjjo1g1jpy427b.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "drinks"


class AuthError(Exception):
    """AuthError Exception
    A standardized way to communicate auth failure modes
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Auth Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": 'Authorization header must start with "Bearer".',
            },
            401,
        )
    if len(parts) == 1:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Token not found.",
            },
            401,
        )
    if len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
            },
            401,
        )
    token = parts[1]
    return token


def verify_decode_jwt(token):
    """verify_decode_jwt
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
    """
    with urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json") as jsonurl:
        jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization malformed.",
            },
            400,
        )
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            auth0_domain = f"https://{AUTH0_DOMAIN}/"
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE, issuer=auth0_domain)
            return payload
        except jwt.ExpiredSignatureError as ex:
            raise AuthError(
                {
                    "code": "token_expired",
                    "description": "Token expired.",
                },
                401,
            ) from ex
        except jwt.JWTClaimsError as ex:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. Please, check the audience and issuer.",
                },
                401,
            ) from ex
        except Exception as ex:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            ) from ex
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


def check_permissions(permissions, payload):
    """check_permissions"""
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT.",
            },
            400,
        )
    if permissions not in payload["permissions"]:
        raise AuthError(
            {
                "code": "unauthorized",
                "description": "Permission not found.",
            },
            403,
        )
    return True


def requires_auth(permissions=""):
    """requires_auth decorator method"""

    def requires_auth_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permissions, payload)
            return func(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator
