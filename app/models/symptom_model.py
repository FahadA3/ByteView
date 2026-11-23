from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Symptom(db.Model):
    shorthand = db.Column(db.String(50), primary_key=True)
    formal_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Symptom {self.shorthand}>'