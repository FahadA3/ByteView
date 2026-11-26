from flask import Blueprint, jsonify
from app.auth import require_auth

bp = Blueprint('auth', __name__, url_prefix = '/auth')

@bp.route('/me', methods = ['GET'])
@require_auth(mfa = False)
def me():
    return jsonify(
        id = g.user.id,
        username = g.user.username,
        role = g.user.role,
        mfa_complete = g.claims.get('aal') == 'aal2',
    )