from flask import Blueprint, jsonify
from app.auth import require_auth
from app.db import db

bp = Blueprint('symptoms', __name__, url_prefix = '/symtpoms')

@bp.route('', methods = ['GET'])
@require_auth
def list_symptoms():
    # Implement your login logic here
    pass

@bp.route('/<string:shorthand>', methods =['GET'])
@require_auth
def get_symptoms(shorthand):
    # Implement your login logic here
    pass
