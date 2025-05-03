from flask import Blueprint, request, jsonify
from app.models.discount import Discount
from app.extensions import db
from datetime import datetime

discount_bp = Blueprint('discount_bp', __name__)

# Get all discounts
@discount_bp.route('/', methods=['GET'])
def get_discounts():
    discounts = Discount.query.all()
    result = [d.to_dict() for d in discounts]
    return jsonify(result), 200

# Get discount by ID
@discount_bp.route('/<int:discount_id>', methods=['GET'])
def get_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    return jsonify(discount.to_dict()), 200

# Create new discount
@discount_bp.route('/', methods=['POST'])
def create_discount():
    data = request.get_json()

    discount = Discount(
        name=data.get('name'),
        description=data.get('description'),
        percentage=data.get('percentage'),
        valid_from=datetime.strptime(data.get('valid_from'), '%Y-%m-%d'),
        valid_to=datetime.strptime(data.get('valid_to'), '%Y-%m-%d')
    )

    db.session.add(discount)
    db.session.commit()
    return jsonify(discount.to_dict()), 201

# Update discount
@discount_bp.route('/<int:discount_id>', methods=['PUT'])
def update_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    data = request.get_json()

    discount.name = data.get('name', discount.name)
    discount.description = data.get('description', discount.description)
    discount.percentage = data.get('percentage', discount.percentage)

    if 'valid_from' in data:
        discount.valid_from = datetime.strptime(data.get('valid_from'), '%Y-%m-%d')
    if 'valid_to' in data:
        discount.valid_to = datetime.strptime(data.get('valid_to'), '%Y-%m-%d')

    db.session.commit()
    return jsonify(discount.to_dict()), 200

# Delete discount
@discount_bp.route('/<int:discount_id>', methods=['DELETE'])
def delete_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    db.session.delete(discount)
    db.session.commit()
    return jsonify({'message': 'Discount deleted'}), 200