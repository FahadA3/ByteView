from flask import Blueprint, request, jsonify, g
from app.auth import require_auth, require_role
from app.db import db

bp = Blueprint('review', __name__, url_prefix = '/review')

@bp.route('/staging/queue', methods =['GET'])
@require_auth
@require_role('Dentist')
def staging_queue():
    # Implement your staging queue logic here
    pass

@bp.route('/<int:edit_id>', methods =['GET'])
@require_auth
@require_role('Dentist')
def get_staged_edit(edit_id):
    # Implement your staging queue logic here
    pass

@bp.route('/<int:edit_id>', methods =['PUT'])
@require_auth
@require_role('Dentist')
def edit(edit_id):
    # Implement your edit logic here
    pass

@bp.route('/<int:edit_id>/approve', methods =['POST'])
@require_auth
@require_role('Dentist')
def approve(edit_id):
    # Implement your approve logic here
    pass

@bp.route('/<int:edit_id>/reject', methods =['POST'])
@require_auth
@require_role('Dentist')
def reject(edit_id):
    # Implement your reject logic here
    pass