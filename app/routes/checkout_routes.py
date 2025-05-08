from flask import Blueprint, request, jsonify
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.extensions import db
from datetime import datetime

checkout_bp = Blueprint('checkout_bp', __name__)

@checkout_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.json

    # Validasi field wajib
    required_fields = ['user_id', 'shipping_address_id', 'billing_address_id', 'order_items', 'payment']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    try:
        # Hitung total amount dari semua order item
        order_items_data = data['order_items']
        total_amount = 0
        order_items = []

        for item_data in order_items_data:
            quantity = item_data['quantity']
            unit_price = item_data['unit_price']
            discount_amount = item_data.get('discount_amount', 0)
            total_price = (quantity * unit_price) - discount_amount

            total_amount += total_price

            order_item = OrderItem(
                product_id=item_data['product_id'],
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                discount_amount=discount_amount
            )
            order_items.append(order_item)

        # Buat order
        new_order = Order(
            user_id=data['user_id'],
            shipping_address_id=data['shipping_address_id'],
            billing_address_id=data['billing_address_id'],
            order_date=datetime.now(),
            total_amount=total_amount,
            status='pending'
        )
        db.session.add(new_order)
        db.session.flush()  # dapatkan order_id untuk relasi foreign key

        # Hubungkan order_item dengan order_id
        for item in order_items:
            item.order_id = new_order.order_id
            db.session.add(item)

        # Buat payment
        payment_data = data['payment']
        new_payment = Payment(
            order_id=new_order.order_id,
            payment_method=payment_data['payment_method'],
            payment_status=payment_data['payment_status'],
            amount=total_amount,
            payment_date=datetime.now()
        )
        db.session.add(new_payment)

        db.session.commit()

        return jsonify({
            'order_id': new_order.order_id,
            'user_id': new_order.user_id,
            'total_amount': total_amount,
            'status': new_order.status,
            'payment': new_payment.as_dict(),
            'items': [item.as_dict() for item in order_items]
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
