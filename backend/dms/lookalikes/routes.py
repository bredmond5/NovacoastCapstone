from flask import Blueprint, abort, jsonify

from .models import Lookalike

blueprint = Blueprint('lookalikes', __name__)


@blueprint.route('/', methods=['GET'])
def index():
    return jsonify(
        count=Lookalike.query.count(),
        results=[lookalike.serialize() for lookalike in Lookalike.query.all()],
    )


@blueprint.route('/<int:id>', methods=['GET'])
def get(id):
    lookalike = Lookalike.query.get(id)
    if lookalike is None:
        abort(404)
    return jsonify(lookalike.serialize())
