from datetime import datetime

from sqlalchemy.sql import func

from dms.db import db


class Lookalike(db.Model):
    """Information about a domain lookalike."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    ip_address = db.Column(db.String(), nullable=False)
    domain_id = db.Column(
        db.Integer,
        db.ForeignKey('domain.id'),
        nullable=False,
    )
    domain = db.relationship('Domain', backref='lookalikes')
    found_on = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.now(),
    )
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    creation_date = db.Column(db.DateTime(), nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'ipAddress': self.ip_address,
            'domainId': self.domain_id,
            'foundOn': self.found_on.isoformat(),
            'creationDate': (
                self.creation_date.isoformat()
                if self.creation_date is not None
                else None
            ),
            'updatedAt': self.updated_at.isoformat(),
        }

    def __repr__(self):
        return f'<Lookalike {self.id} "{self.name}">'
