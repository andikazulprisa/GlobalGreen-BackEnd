from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.address import Address
from app.models.payment import Payment
from app.models.order import Order
from app.models.order_item import OrderItem
from datetime import datetime

checkout_bp = Blueprint('checkout_bp', __name__)

@checkout_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()

    user_id = data.get("user_id")
    shipping_address_data = data.get("shipping_address")
    billing_address_data = data.get("billing_address")
    payment_method = data.get("payment_method")

    if not user_id or not shipping_address_data or not billing_address_data or not payment_method:
        return jsonify({"message": "Missing required fields"}), 400

    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        return jsonify({"message": "Cart is empty"}), 400

    total_amount = 0
    order_items = []

    for item in cart.items:
        product = item.product
        quantity = item.quantity

        # Hitung harga awal
        price = product.price
        discount_amount = 0

        # Cek apakah ada diskon aktif dan berlaku
        if product.discount and product.discount.is_active:
            now = datetime.utcnow()
            if product.discount.valid_from <= now <= product.discount.valid_to:
                if product.discount.discount_type == "percentage":
                    discount_amount = price * (product.discount.discount_value / 100)
                elif product.discount.discount_type == "fixed":
                    discount_amount = product.discount.discount_value

        final_price = max(price - discount_amount, 0)
        total_amount += final_price * quantity

        order_item = OrderItem(
            product_id=product.product_id,
            quantity=quantity,
            price=final_price
        )
        order_items.append(order_item)

    # Simpan shipping address
    shipping_address = Address(user_id=user_id, **shipping_address_data)
    db.session.add(shipping_address)

    # Simpan billing address
    billing_address = Address(user_id=user_id, **billing_address_data)
    db.session.add(billing_address)
    db.session.commit()

    # Buat order
    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        shipping_address_id=shipping_address.address_id,
        billing_address_id=billing_address.address_id
    )
    db.session.add(order)
    db.session.commit()

    # Simpan order items
    for item in order_items:
        item.order_id = order.order_id
        db.session.add(item)

    # Simpan payment
    payment = Payment(
        order_id=order.order_id,
        payment_method=payment_method,
        amount=total_amount,
        payment_status="pending"
    )
    db.session.add(payment)

    # Kosongkan cart
    for item in cart.items:
        db.session.delete(item)

    db.session.commit()

    return jsonify({
        "message": "Checkout successful",
        "order_id": order.order_id,
        "total_amount": total_amount
    }), 201
