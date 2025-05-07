from flask import Blueprint, request, jsonify
from app.models.order_item import OrderItem
from app.models.order import Order
from app.models.product import Product
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

    required_fields = ['order_id', 'product_id', 'quantity', 'unit_price']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    # ✅ Validasi order dan product
    if not Order.query.get(data['order_id']):
        return jsonify({'error': 'Invalid order_id'}), 400
    if not Product.query.get(data['product_id']):
        return jsonify({'error': 'Invalid product_id'}), 400

    # ✅ Hitung total_price
    quantity = data['quantity']
    unit_price = data['unit_price']
    discount_amount = data.get('discount_amount', 0.0)
    total_price = (quantity * unit_price) - discount_amount

    item = OrderItem(
        order_id=data['order_id'],
        product_id=data['product_id'],
        quantity=quantity,
        unit_price=unit_price,
        total_price=total_price,
        discount_amount=discount_amount
    )

    db.session.add(item)
    db.session.commit()
    return jsonify(item.as_dict()), 201

@order_item_bp.route('/<int:item_id>', methods=['PUT'])
def update_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    data = request.json

    # Optional: validasi kalau user ingin ganti order_id / product_id
    if 'order_id' in data and not Order.query.get(data['order_id']):
        return jsonify({'error': 'Invalid order_id'}), 400
    if 'product_id' in data and not Product.query.get(data['product_id']):
        return jsonify({'error': 'Invalid product_id'}), 400

    for key, value in data.items():
        setattr(item, key, value)

    # Rehitung total_price jika quantity/unit_price/discount_amount berubah
    quantity = data.get('quantity', item.quantity)
    unit_price = data.get('unit_price', item.unit_price)
    discount_amount = data.get('discount_amount', item.discount_amount)
    item.total_price = (quantity * unit_price) - discount_amount

    db.session.commit()
    return jsonify(item.as_dict())

@order_item_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_order_item(item_id):
    item = OrderItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Order item deleted'})
