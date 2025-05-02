from flask import Blueprint, request, jsonify
from app.models.wishlist import Wishlist
from app.extensions import db

wishlist_bp = Blueprint('wishlist_bp', __name__)

@wishlist_bp.route('/', methods=['GET'])
def get_all_wishlists():
    wishlists = Wishlist.query.all()
    return jsonify([w.as_dict() for w in wishlists])

@wishlist_bp.route('/<int:wishlist_id>', methods=['GET'])
def get_wishlist(wishlist_id):
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    return jsonify(wishlist.as_dict())

@wishlist_bp.route('/', methods=['POST'])
def create_wishlist():
    data = request.json
    wishlist = Wishlist(**data)
    db.session.add(wishlist)
    db.session.commit()
    return jsonify(wishlist.as_dict()), 201

@wishlist_bp.route('/<int:wishlist_id>', methods=['PUT'])
def update_wishlist(wishlist_id):
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    data = request.json
    for key, value in data.items():
        setattr(wishlist, key, value)
    db.session.commit()
    return jsonify(wishlist.as_dict())

@wishlist_bp.route('/<int:wishlist_id>', methods=['DELETE'])
def delete_wishlist(wishlist_id):
    wishlist = Wishlist.query.get_or_404(wishlist_id)
    db.session.delete(wishlist)
    db.session.commit()
    return jsonify({'message': 'Wishlist deleted'})