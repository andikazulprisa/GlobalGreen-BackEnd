from flask import Blueprint, request, jsonify
from app.models.user import User
from app.extensions import db

user_bp = Blueprint('user_bp', __name__)

# GET /users
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

# GET /users/<id>
@user_bp.route('/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(user.as_dict())

# POST /users
@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        email=data['email'],
        password=data['password'], 
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        phone=data.get('phone'),
        role=data.get('role', 'Customer')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# PUT /users/<id>
@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.get_json()
    user.email = data['email']
    user.password = data['password'] 
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    user.phone = data.get('phone', user.phone)
    user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# DELETE /users/<id>
@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Dummy db
@user_bp.route('/dummy', methods=['GET'])
def get_dummy_users():
    dummy_users = [
        {
            "id": 1,
            "email": "nNj6u@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890",
            "role": "Customer"
        },
        {
            "id": 2,
            "email": "t2hYH@example.com",
            "first_name": "Jane",
            "last_name": "Doe", 
            "phone": "9876543210",
            "role": "Admin"        
        }
    ]