from flask import Blueprint, request, jsonify, g
from app.auth import require_auth
from app.db import db

bp = Blueprint('record', __name__, url_prefix = '/record')

@bp.route('/<int:patient_id>', methods =['GET'])
@require_auth
def get_record(patient_id): 
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>/symptoms', methods =['POST'])
@require_auth
def add_symptom(patient_id): 
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>/tooth/<int:tooth_number>', methods =['GET'])
@require_auth
def get_tooth(patient_id, tooth_number): 
    # Implement your register logic here
    pass

@bp.route('/<int:patient_id>/tooth/<int:tooth_number>/history', methods =['GET'])
@require_auth
def get_tooth_history(patient_id, tooth_number):
    # Implement your register logic here
    pass