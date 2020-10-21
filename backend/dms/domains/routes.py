import logging

from flask import Blueprint, abort, jsonify, request
from sqlalchemy import or_

from .models import Domain, db
from dms.util import import_csv_view
from dms.groups.models import Group

blueprint = Blueprint('domains', __name__)

logger = logging.Logger(__name__)


@blueprint.route('/', methods=['GET'])
def domain_index():
    domains = Domain.query
    params = request.get_json()
    if params is not None and 'q' in params:
        q = request.json['q']
        if isinstance(q, dict):
            domains = domains.filter(
                Domain.name.ilike(f"%{q.get('name', '')}%"),
            )
        else:
            domains = domains.filter(or_(
                Domain.name.ilike(f"%{q}%"),
            ))
    domains = domains.all()
    return jsonify(
        count=len(domains),
        results=[d.serialize() for d in domains],
    )


@blueprint.route('/', methods=['POST'])
def domain_create():
    data = request.get_json()
    if data is None or 'name' not in data or 'groupId' not in data:
        abort(400)
    d = Domain(name=data['name'], group_id=data['groupId'])
    if 'active' in data:
        d.active = data['active']
    db.session.add(d)
    db.session.commit()
    logger.info(f'Created new domain: {d}')
    return jsonify(d.serialize()), 201


@blueprint.route('/<int:id>', methods=['GET'])
def domain_get(id):
    d = Domain.query.get(id)
    if d is None:
        abort(404)
    return jsonify(d.serialize())


@blueprint.route('/<int:id>', methods=['PUT'])
def domain_update(id):
    data = request.get_json()
    if data is None:
        abort(400)
    d = Domain.query.get(id)
    if 'name' in data:
        d.name = data['name']
    if 'groupId' in data:
        d.group_id = data['groupId']
    if 'active' in data:
        d.active = data['active']
    db.session.commit()
    logger.info(f'Updated domain: {d}')
    return jsonify(Group.query.get(id).serialize())


@blueprint.route('/<int:id>', methods=['DELETE'])
def domains_delete(id):
    d = Domain.query.get(id)
    if d is None:
        abort(404)
    data = d.serialize()
    db.session.delete(d)
    db.session.commit()
    logger.info(f'Deleted domain: {d}')
    return jsonify(data)


@blueprint.route('/import-csv', methods=['POST'])
def csv_import():
    return import_csv_view(
        Domain,
        required_fields=['name', 'group_id'],
        optional_fields=['active', 'scan_period'],
    )
