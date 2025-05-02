from flask import Blueprint, request, jsonify
from app.models.category import Category
from app.extensions import db

category_bp = Blueprint('category_bp', __name__)

@category_bp.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([category.as_dict() for category in categories])

@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.as_dict())

@category_bp.route('/', methods=['POST'])
def create_category():
    data = request.json
    category = Category(**data)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.as_dict()), 201

@category_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    data = request.json
    for key, value in data.items():
        setattr(category, key, value)
    db.session.commit()
    return jsonify(category.as_dict())

@category_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Category deleted'})