import os
from functools import wraps
from uuid import UUID

import jwt
from flask import request, jsonify, g

from app.models import User

SUPABASE_URL = os.environ['SUPABASE_URL']
ISSUER = f'{SUPABASE_URL}/auth/v1'
jwks_client = jwt.PyJWKClient(f'{ISSUER}/.well-known/jwks.json')  # caches keys


def _decode_token():
    header = request.headers.get('Authorization', '')
    if not header.startswith('Bearer '):
        return None
    token = header.removeprefix('Bearer ')
    try:
        key = jwks_client.get_signing_key_from_jwt(token).key
        return jwt.decode(
            token, key,
            algorithms=['ES256', 'RS256'],
            audience='authenticated',
            issuer=ISSUER,
        )
    except jwt.PyJWTError:
        return None


def require_auth(f=None, *, mfa=True):
    """Use as @require_auth or @require_auth(mfa=False)."""
    if f is None:
        return lambda func: require_auth(func, mfa=mfa)

    @wraps(f)
    def wrapper(*args, **kwargs):
        claims = _decode_token()
        if claims is None:
            return jsonify(error='Not authenticated'), 401
        if mfa and claims.get('aal') != 'aal2':
            return jsonify(error='MFA required'), 401

        user = User.query.filter_by(auth_id=UUID(claims['sub'])).first()
        if user is None or not user.is_active:
            return jsonify(error='No active ByteView account'), 403

        g.user = user
        g.claims = claims
        return f(*args, **kwargs)
    return wrapper


def require_role(*roles):
    """Must go BELOW @require_auth so g.user is already set."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if g.user.role not in roles:
                return jsonify(error='Forbidden'), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator