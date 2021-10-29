from database import db
from uuid import uuid4
from werkzeug.security import check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    active = db.Column(db.Boolean(), default=True)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def serialize(self):
        return {
                'id': self.id,
                'email': self.email,
                'active': self.active
                }
