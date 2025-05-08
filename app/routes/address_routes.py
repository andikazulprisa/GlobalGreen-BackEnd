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
    required_fields = ['user_id', 'address_type', 'street_address']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    new_address = Address(**data)
    db.session.add(new_address)
    db.session.commit()
    return jsonify(new_address.serialize()), 201
def update_address(id):
    address = Address.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(address, key, value)
    db.session.commit()
    return jsonify(address.serialize())

@address_bp.route('/<int:id>', methods=['DELETE'])
def delete_address(id):
    address = Address.query.get_or_404(id)
    db.session.delete(address)
    db.session.commit()
    return jsonify({"message": "Address deleted"})