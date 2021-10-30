from uuid import uuid4
from database import db
from sqlalchemy.orm import relationship, backref
from werkzeug.security import check_password_hash


class User:
    __tablename__ = 'users'

    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
    email = db.Column(db.String(84), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=True)
    request = relationship("Groups", backref=backref("groups", uselist=False))

    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def serialize(self):
        return {
                'id': self.id,
                'email': self.email,
                'active': self.active
                }
