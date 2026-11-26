from flask_sqlalchemy import SQLAlchemy
ROOT = '/patients'

@require_auth
@app.route(ROOT + '/search', methods =[GET])
def search(): 
    # Implement your search logic here
    pass

@require_auth
@app.route(ROOT + '/register', methods =[POST])
def register(): 
    # Implement your register logic here
    pass

@require_auth
@app.route(ROOT + '/<int:patient_id>', methods =[GET])
def get_patient(patient_id): 
    # Implement your register logic here
    pass

@require_auth
@app.route(ROOT + '/<int:patient_id>', methods =[PUT])
def update_patient(patient_id): 
    # Implement your register logic here
    pass

@require_auth
@require_role('Dentist')
@app.route(ROOT + '/<int:patient_id>/deactivate', methods =[POST])
def deactivate_patient(patient_id):
    # Implement your register logic here
    pass

@require_auth
@app.route(ROOT + '/<int:patient_id>/history', methods =[GET])
def view_history(patient_id): 
    # Implement your view history logic here
    pass

