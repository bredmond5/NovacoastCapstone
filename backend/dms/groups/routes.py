import logging
from datetime import datetime

from flask import Blueprint, abort, jsonify, request
from sqlalchemy import or_

from dms.util import import_csv_view

from .models import Group, db

blueprint = Blueprint('groups', __name__)

logger = logging.Logger(__name__)


@blueprint.route('/', methods=['GET'])
def group_index():
    groups = Group.query
    params = request.get_json()
    if params is not None and 'q' in params:
        q = request.json['q']
        if isinstance(q, dict):
            groups = groups.filter(
                Group.name.ilike(f"%{q.get('name', '')}%"),
                Group.emails.ilike(f"%{q.get('emails', '')}%"),
            )
        else:
            groups = groups.filter(or_(
                Group.name.ilike(f'%{q}%'),
                Group.emails.ilike(f'%{q}%'),
            ))
    groups = groups.all()
    return jsonify(
        count=len(groups),
        results=[g.serialize() for g in groups],
    )


@blueprint.route('/', methods=['POST'])
def group_create():
    data = request.get_json()
    if data is None or 'emails' not in data or 'name' not in data:
        abort(400)
    group = Group(name=data['name'], emails=data['emails'])
    if 'recur' in data:
        group.recur = data['recur']
    if 'startAt' in data:
        group.start_at = datetime.fromisoformat(data['startAt'])
    if 'timeZone' in data:
        group.time_zone = data['timeZone']
    db.session.add(group)
    db.session.commit()
    logger.info(f"Created new group: {group}")
    return jsonify(group.serialize()), 201


@blueprint.route('/<int:id>', methods=['GET'])
def group_get(id):
    g = Group.query.get(id)
    if g is None:
        abort(404)
    return jsonify(g.serialize())


@blueprint.route('/<int:id>', methods=['PUT'])
def group_update(id):
    data = request.get_json()
    if data is None:
        abort(400)
    group = Group.query.get(id)
    if 'emails' in data:
        group.emails = data['emails']
    if 'name' in data:
        group.name = data['name']
    if 'recur' in data:
        group.recur = data['recur']
    if 'startAt' in data:
        group.start_at = datetime.fromisoformat(data['startAt'])
    if 'timeZone' in data:
        group.time_zone = data['timeZone']
    db.session.commit()
    logger.info(f'Updated group: {group}')
    return jsonify(group.serialize())


@blueprint.route('/<int:id>', methods=['DELETE'])
def group_delete(id):
    g = Group.query.get(id)
    if g is None:
        abort(404)
    data = g.serialize()
    db.session.delete(g)
    db.session.commit()
    logger.info(f'Deleted group: {g}')
    return jsonify(data)


@blueprint.route('/import-csv', methods=['POST'])
def import_csv():
    return import_csv_view(
        Group,
        required_fields=['name', 'emails'],
        optional_fields=[],
    )
