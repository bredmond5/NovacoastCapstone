from pytz import timezone
from pytz.exceptions import UnknownTimeZoneError
from sqlalchemy.orm import validates
from sqlalchemy.sql import func

from dms.db import db


class Group(db.Model):
    """Represents a group, which is a set of email addresses."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    # Semicolon seperated list of email addresses
    emails = db.Column(db.Text(), nullable=False)

    start_at = db.Column(
        db.DateTime(),
        nullable=False,
        server_default=func.now(),
    )
    recur = db.Column(
        db.String(),
        nullable=False,
        server_default='daily'
    )
    time_zone = db.Column(db.String(), nullable=False, server_default='UTC')
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
            'emails': self.emails,
            'startAt': self.start_at.isoformat(),
            'recur': self.recur,
            'timeZone': self.time_zone,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat(),
        }

    @validates('recur')
    def validate_recur(self, key, recur):
        if recur not in ['daily', 'weekly', 'monthly']:
            raise ValueError()
        return recur

    @validates('start_at')
    def validate_start_at(self, key, start_at):
        start_at = start_at.replace(microsecond=0)
        return start_at

    @validates('time_zone')
    def validate_time_zone(self, key, time_zone):
        try:
            timezone(time_zone)
        except UnknownTimeZoneError:
            raise ValueError('Invalid IANA time zone name')
        return time_zone

    def tz(self):
        return timezone(self.time_zone)

    def start_at_with_tz(self):
        return self.start_at.replace(tzinfo=self.tz())

    def __repr__(self):
        return f'<Group {self.id} "{self.name}">'
