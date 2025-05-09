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

    print("New cart created:", new_cart.serialize())  # Debugging line

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

# Ambil Cart berdasarkan user_id
@cart_bp.route('/user/<int:user_id>', methods=['GET'])
def get_carts_by_user(user_id):
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({"message": "Cart not found for this user"}), 404
    return jsonify(cart.serialize()), 200