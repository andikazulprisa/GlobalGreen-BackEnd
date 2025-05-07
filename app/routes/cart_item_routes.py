from flask import Blueprint, request, jsonify
from app.models.cart_item import CartItem
from app.extensions import db

cart_item_bp = Blueprint('cart_item_bp', __name__)

@cart_item_bp.route('/', methods=['GET'])
def get_cart_items():
    items = CartItem.query.all()
    return jsonify([item.serialize() for item in items])

@cart_item_bp.route('/', methods=['POST'])
def create_cart_item():
    data = request.json
    try:
        new_item = CartItem(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify(new_item.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@cart_item_bp.route('/<int:id>', methods=['PUT'])
def update_cart_item(id):
    item = CartItem.query.get_or_404(id)
    try:
        for key, value in request.json.items():
            setattr(item, key, value)
        db.session.commit()
        return jsonify(item.serialize())
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@cart_item_bp.route('/<int:id>', methods=['DELETE'])
def delete_cart_item(id):
    item = CartItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Cart item deleted"})
