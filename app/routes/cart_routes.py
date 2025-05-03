from flask import Blueprint, request, jsonify
from app.models.cart import Cart
from app.extensions import db

cart_bp = Blueprint('cart_bp', __name__)

@cart_bp.route('/', methods=['GET'])
def get_carts():
    carts = Cart.query.all()
    return jsonify([cart.serialize() for cart in carts])

@cart_bp.route('/', methods=['POST'])
def create_cart():
    data = request.json
    new_cart = Cart(**data)
    db.session.add(new_cart)
    db.session.commit()
    return jsonify(new_cart.serialize()), 201

@cart_bp.route('/<int:id>', methods=['PUT'])
def update_cart(id):
    cart = Cart.query.get_or_404(id)
    for key, value in request.json.items():
        setattr(cart, key, value)
    db.session.commit()
    return jsonify(cart.serialize())

@cart_bp.route('/<int:id>', methods=['DELETE'])
def delete_cart(id):
    cart = Cart.query.get_or_404(id)
    db.session.delete(cart)
    db.session.commit()
    return jsonify({"message": "Cart deleted"})