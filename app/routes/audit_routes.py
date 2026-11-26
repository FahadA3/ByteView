from functools import wraps
from flask import blueprint, request, jsonify, session
import jwt
from app.db import db
from sqlalchemy import text

ROOT = 'audit'

@require_auth
@require_role('Dentist')
@app.route(ROOT + '/patient/<int:patient_id>', methods =[GET])
def get_patient_audit_log(patient_id):
    # Implement your login logic here
    pass