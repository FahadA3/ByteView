from flask_sqlalchemy import SQLAlchemy
ROOT = '/record'

@require_auth
@require_role('Dentist')
@app.route(ROOT + '/staging/queue', methods =[GET])
def staging_queue():
    # Implement your staging queue logic here
    pass

@require_auth
@require_role('Dentist')
@app.route(ROOT + '/review/<int:edit_id>', methods =[GET])
def get_staging_queue():
    # Implement your staging queue logic here
    pass

@require_auth
@require_role('Dentist')
@app.route(ROOT + '/<int:edit_id>', methods =[PUT])
def edit(edit_id):
    # Implement your edit logic here
    pass

@require_auth
@require_role('Dentist')
@app.route(ROOT + '/<int:edit_id>/approve', methods =[POST])
def approve(edit_id):
    # Implement your approve logic here
    pass

@require_auth
@require_role('Dentist')
@app.route(ROOT + '<int:edit_id>/reject', methods =[POST])
def reject(edit_id):
    # Implement your reject logic here
    pass