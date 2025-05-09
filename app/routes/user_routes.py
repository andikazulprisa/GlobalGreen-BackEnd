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
    try:
        new_user = User(
            email=data['email'],
            password=data['password'], 
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            image_url=data.get('image_url'),
            role=data.get('role', 'Customer')
        )
        db.session.add(new_user)
        db.session.commit()
        print(">>> User berhasil disimpan ke DB")
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        print(">>> ERROR:", str(e))
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# ✅ PUT /users/<id> — versi perbaikan
@user_bp.route('/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()

    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'phone' in data:
        user.phone = data['phone']
    if 'image_url' in data:
        user.image_url = data['image_url']
    if 'role' in data:
        user.role = data['role']

    try:
        db.session.commit()
        return jsonify({'message': 'User updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# DELETE /users/<id>
@user_bp.route('/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

