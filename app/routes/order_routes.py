from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.models.user import User
from app.models.address import Address
from app.extensions import db
from datetime import datetime

order_bp = Blueprint('order_bp', __name__)

@order_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([o.as_dict() for o in orders])

@order_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.as_dict())

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json

    required_fields = ['user_id', 'shipping_address_id', 'billing_address_id']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # ✅ Validasi foreign key
    if not User.query.get(data['user_id']):
        return jsonify({'error': 'Invalid user_id'}), 400

    if not Address.query.get(data['shipping_address_id']):
        return jsonify({'error': 'Invalid shipping_address_id'}), 400

    if not Address.query.get(data['billing_address_id']):
        return jsonify({'error': 'Invalid billing_address_id'}), 400

    order = Order(
        user_id=data['user_id'],
        shipping_address_id=data['shipping_address_id'],
        billing_address_id=data['billing_address_id'],
        delivery_date=data.get('delivery_date'),
        status=data.get('status', 'pending'),
        total_amount=data.get('total_amount', 0.0),  # Optional: bisa diupdate saat order_items ditambahkan
        order_date=datetime.now()
    )

    db.session.add(order)
    db.session.commit()
    return jsonify(order.as_dict()), 201

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json

    if 'user_id' in data and not User.query.get(data['user_id']):
        return jsonify({'error': 'Invalid user_id'}), 400

    if 'shipping_address_id' in data and not Address.query.get(data['shipping_address_id']):
        return jsonify({'error': 'Invalid shipping_address_id'}), 400

    if 'billing_address_id' in data and not Address.query.get(data['billing_address_id']):
        return jsonify({'error': 'Invalid billing_address_id'}), 400

    for key, value in data.items():
        setattr(order, key, value)

    db.session.commit()
    return jsonify(order.as_dict())

@order_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'})
