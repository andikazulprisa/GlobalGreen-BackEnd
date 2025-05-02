from flask import Blueprint, request, jsonify
from app.models.wishlist_item import WishlistItem
from app.extensions import db

wishlist_item_bp = Blueprint('wishlist_item_bp', __name__)

@wishlist_item_bp.route('/', methods=['GET'])
def get_all_wishlist_items():
    items = WishlistItem.query.all()
    return jsonify([i.as_dict() for i in items])

@wishlist_item_bp.route('/<int:item_id>', methods=['GET'])
def get_wishlist_item(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    return jsonify(item.as_dict())

@wishlist_item_bp.route('/', methods=['POST'])
def create_wishlist_item():
    data = request.json
    item = WishlistItem(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.as_dict()), 201

@wishlist_item_bp.route('/<int:item_id>', methods=['PUT'])
def update_wishlist_item(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    data = request.json
    for key, value in data.items():
        setattr(item, key, value)
    db.session.commit()
    return jsonify(item.as_dict())

@wishlist_item_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_wishlist_item(item_id):
    item = WishlistItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Wishlist item deleted'})