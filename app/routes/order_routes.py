from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.extensions import db

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
    order = Order(**data)
    db.session.add(order)
    db.session.commit()
    return jsonify(order.as_dict()), 201

@order_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    data = request.json
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