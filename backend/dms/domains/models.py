from sqlalchemy.sql import func

from dms.db import db


class Domain(db.Model):
    """A domain and associated settings."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)
    group_id = db.Column(
        db.Integer,
        db.ForeignKey('group.id'),
        nullable=False,
    )
    group = db.relationship('Group', backref='domains')
    last_emailed = db.Column(db.DateTime(), nullable=True)
    active = db.Column(db.Boolean(), nullable=False, default=True)
    last_scanned = db.Column(db.DateTime(), nullable=True)
    num_of_scans = db.Column(db.Integer(), nullable=False, server_default='0')
    created_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'groupId': self.group_id,
            'lastEmailed': (
                self.last_emailed.isoformat()
                if self.last_emailed is not None
                else None
            ),
            'active': self.active,
            'lastScanned': (
                self.last_scanned.isoformat()
                if self.last_scanned is not None
                else None
            ),
            'numberOfScans': self.num_of_scans,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f'<Domain {self.id} "{self.name}">'
