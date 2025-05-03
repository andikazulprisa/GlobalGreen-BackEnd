from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.extensions import db

product_bp = Blueprint('product_bp', __name__)

@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.as_dict() for product in products])

@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product.as_dict())

@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        category_id=data['category_id'],
        price=data['price'],
        unit_type=data.get('unit_type'),
        stock_quantity=data['stock_quantity'],
        image_url=data.get('image_url'),
        organic=data.get('organic', False)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    data = request.get_json()
    product.name = data['name']
    product.description = data.get('description', product.description)
    product.category_id = data['category_id']
    product.price = data['price']
    product.unit_type = data.get('unit_type', product.unit_type)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.image_url = data.get('image_url', product.image_url)
    product.organic = data.get('organic', product.organic)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})