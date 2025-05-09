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

    try:
        discount = Discount(
            code=data.get('code'),
            description=data.get('description'),
            discount_type=data.get('discount_type'),  # "percentage" or "fixed"
            discount_value=data.get('discount_value'),
            valid_from=datetime.strptime(data.get('valid_from'), '%Y-%m-%d') if data.get('valid_from') else None,
            valid_to=datetime.strptime(data.get('valid_to'), '%Y-%m-%d') if data.get('valid_to') else None,
            is_active=data.get('is_active', True)
        )

        db.session.add(discount)
        db.session.commit()
        return jsonify(discount.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# Update discount
@discount_bp.route('/<int:discount_id>', methods=['PUT'])
def update_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    data = request.get_json()

    discount.code = data.get('code', discount.code)
    discount.description = data.get('description', discount.description)
    discount.discount_type = data.get('discount_type', discount.discount_type)
    discount.discount_value = data.get('discount_value', discount.discount_value)
    discount.is_active = data.get('is_active', discount.is_active)

    if 'valid_from' in data:
        discount.valid_from = datetime.strptime(data['valid_from'], '%Y-%m-%d')
    if 'valid_to' in data:
        discount.valid_to = datetime.strptime(data['valid_to'], '%Y-%m-%d')

    db.session.commit()
    return jsonify(discount.to_dict()), 200

# Delete discount
@discount_bp.route('/<int:discount_id>', methods=['DELETE'])
def delete_discount(discount_id):
    discount = Discount.query.get_or_404(discount_id)
    db.session.delete(discount)
    db.session.commit()
    return jsonify({'message': 'Discount deleted'}), 200
