from flask import Blueprint, request, jsonify
from app.models.address import Address
from app.extensions import db

address_bp = Blueprint('address_bp', __name__)

@address_bp.route('/', methods=['GET'])
def get_addresses():
    addresses = Address.query.all()
    return jsonify([addr.serialize() for addr in addresses])

@address_bp.route('/', methods=['POST'])
def create_address():
    data = request.json
    new_address = Address(**data)
    db.session.add(new_address)
    db.session.commit()
    return jsonify(new_address.serialize()), 201

@address_bp.route('/<int:id>', methods=['PUT'])
def update_address(id):
    address = Address.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(address, key, value)
    db.session.commit()
    return jsonify(address.serialize())

@address_bp.route('/addresses/<int:id>', methods=['DELETE'])
def delete_address(id):
    address = Address.query.get_or_404(id)
    db.session.delete(address)
    db.session.commit()
    return jsonify({"message": "Address deleted"})