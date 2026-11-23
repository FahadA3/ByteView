from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class User (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    auth_id = db.Column(db.UUID(as_uuid=True), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)

    def is_dentist(self):
        return self.role == 'Dentist'

    def is_dental_assistant(self):
        return self.role == 'Dental Assistant'

    def __repr__(self):
        return f'<User {self.username} ({self.role})>' 