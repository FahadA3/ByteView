from functools import wraps
from flask import blueprint, request, jsonify, session
import jwt
from app.db import db
from sqlalchemy import text

ROOT = '/symptoms'

@require_auth
@app.route(ROOT, methods =[GET])
def list_symptoms():
    # Implement your login logic here
    pass

@require_auth
@app.route(ROOT + '/<string:shorthand>', methods =[GET])
def get_symptoms(shorthand):
    # Implement your login logic here
    pass
