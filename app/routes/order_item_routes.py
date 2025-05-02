from flask import Blueprint, request, jsonify
from app.models.order_item import OrderItem
from app.extensions import db

order_item_bp = Blueprint('order_item_bp', __name__)

@order_item_bp.route('/', methods=['GET'])
def get_order_items():
    items = OrderItem.query.all()
    return jsonify([item.as_dict() for item in items])

@order_item_bp.route('/<int:item_id>', methods=['GET'])
def get_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    return jsonify(item.as_dict())

@order_item_bp.route('/', methods=['POST'])
def create_order_item():
    data = request.json
    item = OrderItem(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.as_dict()), 201

@order_item_bp.route('/<int:item_id>', methods=['PUT'])
def update_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    data = request.json
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify(item.as_dict())

@order_item_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Order item deleted'})