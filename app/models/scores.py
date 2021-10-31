from uuid import uuid4
from database import db


class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    Housing = db.Column(db.Integer(), nullable=False,)
    Salary = db.Column(db.String(84), nullable=False)

    def serialize(self):
        return {
                'id': self.id,
                'name': self.name,
                'active': self.active
                }
