from flask_sqlalchemy import SQLAlchemy

ROOT = '/record'

@require_auth
@app.route(ROOT + '<int:patient_id>', methods =[GET])
def get_record(patient_id): 
    # Implement your register logic here
    pass

@require_auth
@app.route(ROOT + '/record/<int:patient_id>/mouth/symptoms', methods =[GET])
def add_symptom(patient_id):
    # Implement your add symptom logic here
    pass

@require_auth
@app.route(ROOT + '/<int:patient_id>/symptoms', methods =[POST])
def get_mouth_symptoms(patient_id):
    # Implement your get mouth symptoms logic here
    pass

@require_auth
@app.route(ROOT + '/<int:patient_id>/symptoms', methods =[POST])
def add_symptom(patient_id): 
    # Implement your register logic here
    pass

@require_auth
@app.route(ROOT + '<int:patient_id/tooth/<int:tooth_number>', methods =[GET])
def get_tooth(patient_id): 
    # Implement your register logic here
    pass

@require_auth
@app.route(ROOT + '<int:patient_id/tooth/<int:tooth_number>/history', methods =[GET])
def get_tooth_history(patient_id): 
    # Implement your register logic here
    pass