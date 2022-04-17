from db import db
from sqlalchemy import func


class VendorApplication(db.Model):
    __tablename__ = "vendor_application"

    id = db.Column(db.Integer(), primary_key=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    approved = db.Column(db.Boolean(), nullable=True)
    completed_by_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime(timezone=False), server_default=func.now(), nullable=False)
    is_active = db.Column(db.Boolean(), default=True, nullable=False)
    completed_at = db.Column(db.DateTime(timezone=False), nullable=True)

    # Used internally, does not affect table creation
    owner = db.relationship("User", foreign_keys=[owner_id])
    completed_by = db.relationship("User", foreign_keys=[completed_by_id])

    def __init__(self, owner_id, title, description):
        self.owner_id = owner_id
        self.title = title
        self.description = description
