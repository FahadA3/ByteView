from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Patient(db.Model):
    patient_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    first_name_hash = db.Column(db.CHAR(64), nullable=False)
    last_name_hash = db.Column(db.CHAR(64), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    phone = db.Column(db.Text, nullable=True)
    email = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    tooth_record = db.relationship('ToothRecord', backref='patient')
    staged_edits = db.relationship('StagedEdit', backref='patient')
    
    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

    def current_records(self):
        return [record for record in self.tooth_record if record.change_date is None]