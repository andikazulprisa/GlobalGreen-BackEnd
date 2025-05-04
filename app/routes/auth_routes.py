from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from datetime import timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already registered"}), 400
    new_user = User(
        email=data['email'],
        password=data['password'],  # otomatis di-hash via setter
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone'),
        role=data.get('role', 'Customer')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Email atau password salah'}), 401

    access_token = create_access_token(
        identity=user.user_id,
        additional_claims={"role": user.role},
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        'access_token': access_token,
        'user': user.as_dict()
    })

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User not found"}), 404

    return jsonify(user.as_dict()), 200
