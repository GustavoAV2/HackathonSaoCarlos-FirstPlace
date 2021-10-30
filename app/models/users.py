from database import db
from werkzeug.security import check_password_hash
from app.models.base import Base


class User(Base, db.Model):
    __tablename__ = 'users'

    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def serialize(self):
        return {
                'id': self.id,
                'email': self.email,
                'active': self.active
                }
