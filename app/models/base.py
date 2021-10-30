from uuid import uuid4
from database import db


class Base(db.Model):
    id = db.Column(db.String(36), default=lambda: str(uuid4()), primary_key=True)
    active = db.Column(db.Boolean(), default=True)
