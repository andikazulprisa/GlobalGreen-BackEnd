from flask import Blueprint, request, jsonify
from app.models.payment import Payment
from app.extensions import db

payment_bp = Blueprint('payment_bp', __name__)

@payment_bp.route('/', methods=['GET'])
def get_payments():
    payments = Payment.query.all()
    return jsonify([p.as_dict() for p in payments])

@payment_bp.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    return jsonify(payment.as_dict())

@payment_bp.route('/', methods=['POST'])
def create_payment():
    data = request.json
    required_fields = ['order_id', 'payment_method', 'payment_status', 'amount']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    payment = Payment(**data)
    db.session.add(payment)
    db.session.commit()
    return jsonify(payment.as_dict()), 201

@payment_bp.route('/<int:payment_id>', methods=['PUT'])
def update_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    data = request.json
    for key, value in data.items():
        setattr(payment, key, value)
    db.session.commit()
    return jsonify(payment.as_dict())

@payment_bp.route('/<int:payment_id>', methods=['DELETE'])
def delete_payment(payment_id):
    payment = Payment.query.get_or_404(payment_id)
    db.session.delete(payment)
    db.session.commit()
    return jsonify({'message': 'Payment deleted'})