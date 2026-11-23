from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class StagedEdit (db.Model):
    edit_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tooth_number = db.Column(db.Integer, nullable=False)
    edit_payload = db.Column(db.JSONB, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='Staged')
    reviewed_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    patient = db.relationship('Patient', backref=db.backref('staged_edits'))


    def __repr__(self):
        return f'<StagedEdit {self.tooth_number} for {self.patient.first_name} {self.patient.last_name}>'

    def is_pending(self):
        return self.status == 'Staged'