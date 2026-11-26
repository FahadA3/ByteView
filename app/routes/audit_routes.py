from flask import Blueprint, jsonify
from app.auth import require_auth, require_role
from app.db import db

bp = Blueprint('audit', __name__, url_prefix='/audit')

@bp.route('/patient/<int:patient_id>', methods = ['GET'])
@require_auth
@require_role('Dentist')
def get_patient_audit_log(patient_id):
    # Implement your login logic here
    pass