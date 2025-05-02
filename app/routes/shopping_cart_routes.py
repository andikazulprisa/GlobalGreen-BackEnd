from flask import Blueprint, request, jsonify
from app.models.shopping_cart import ShoppingCart
from app.extensions import db

shopping_cart_bp = Blueprint('shopping_cart_bp', __name__)

@shopping_cart_bp.route('/', methods=['GET'])
def get_all_carts():
    carts = ShoppingCart.query.all()
    return jsonify([c.as_dict() for c in carts])

@shopping_cart_bp.route('/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = ShoppingCart.query.get_or_404(cart_id)
    return jsonify(cart.as_dict())

@shopping_cart_bp.route('/', methods=['POST'])
def create_cart():
    data = request.json
    cart = ShoppingCart(**data)
    db.session.add(cart)
    db.session.commit()
    return jsonify(cart.as_dict()), 201

@shopping_cart_bp.route('/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    cart = ShoppingCart.query.get_or_404(cart_id)
    data = request.json
    for key, value in data.items():
        setattr(cart, key, value)
    db.session.commit()
    return jsonify(cart.as_dict())

@shopping_cart_bp.route('/<int:cart_id>', methods=['DELETE'])
def delete_cart(cart_id):
    cart = ShoppingCart.query.get_or_404(cart_id)
    db.session.delete(cart)
    db.session.commit()
    return jsonify({'message': 'Shopping cart deleted'})