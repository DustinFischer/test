import json
from functools import wraps
from urllib.request import urlopen

from flask import request
from jose import jwt

AUTH0_DOMAIN = 'dustin-sso.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee-api'


# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Parse the Bearer [token] Authorization  header"""
    auth_header = request.headers.get('Authorization', None)

    if auth_header is None:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected'
        }, 401)

    auth = auth_header.split()

    if auth[0] != 'Bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with Bearer'
        }, 401)

    if len(auth) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)

    if len(auth) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer token'
        }, 401)

    return auth[1]


def check_permissions(permission, payload):
    perms = payload.get('permissions', None)

    if perms is None:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 403)

    if permission not in perms:
        raise AuthError({
            'code': 'unauthorized',
            'description': 'Permission not found.'
        }, 403)

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')

    try:
        header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Error decoding token headers'
        })

    # Validate claims
    kid = header.get('kid', None)
    if kid is None:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    jwks = json.loads(jsonurl.read())

    # Extract the key
    rsa_key = next(({
        'kty': key['kty'],
        'kid': key['kid'],
        'use': key['use'],
        'n': key['n'],
        'e': key['e']
    } for key in jwks['keys'] if key['kid'] == kid), {})

    if not rsa_key:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Key matching kid claim not found.'
        }, 401)

    try:
        # Verify the JWT, decode the payload
        return jwt.decode(
            token,
            rsa_key,
            algorithms=ALGORITHMS,
            audience=API_AUDIENCE,
            issuer='https://' + AUTH0_DOMAIN + '/'
        )
    except jwt.ExpiredSignatureError:
        raise AuthError({
            'code': 'token_expired',
            'description': 'Token expired.'
        }, 401)
    except jwt.JWTClaimsError:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Incorrect claims.'
                           'Please, check the audience and issuer.'
        }, 401)
    except jwt.JWTError as exc:
        raise AuthError({
            'code': 'invalid_token',
            'description': exc.args[0]
        }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
