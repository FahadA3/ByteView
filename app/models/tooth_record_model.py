from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ToothRecord(db.Model):
    record_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    tooth_number = db.Column(db.Integer, nullable=True)
    gum_decay = db.Column(db.Numeric(3,1), nullable=False, default=False)
    symptom_notes = db.Column(db.Text, nullable=True)
    symptom_codes = db.Column(db.ARRAY(db.String), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    edit_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=True)
    start_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    change_date = db.Column(db.DateTime, nullable=True, onupdate=db.func.current_timestamp())

    patient = db.relationship('Patient', backref=db.backref('tooth_records'))
    author = db.relationship('User', foreign_keys=[user_id], backref=db.backref('created_tooth_records'))


    def __repr__(self):
        return f'<ToothRecord {self.tooth_number} for Patient {self.patient_id}>'

    def is_current(self):
        return self.change_date is None

    def is_wholemouth(self):
        return self.tooth_number is None