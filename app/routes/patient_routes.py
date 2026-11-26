from flask import Blueprint
from app.auth import require_auth, require_role
from app.db import db

bp = Blueprint('patients', __name__, url_prefix = '/patients')

@bp.route('/search', methods =['GET'])
@require_auth
def search(): 
    # Implement your search logic here
    pass

@bp.route('/register', methods =['POST'])
@require_auth
def register():
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>', methods =['GET'])
@require_auth
def get_patient(patient_id): 
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>', methods =['PUT'])
@require_auth
def update_patient(patient_id): 
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>/deactivate', methods =['POST'])
@require_auth
@require_role('Dentist')
def deactivate_patient(patient_id):
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>/history', methods =['GET'])
@require_auth
def view_history(patient_id): 
    # Implement your view history logic here
    pass

