from flask import Blueprint, request, jsonify
from app.models.product import Product
from app.models.order_item import OrderItem
from app.extensions import db

product_bp = Blueprint('product_bp', __name__)

# GET semua produk
@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.as_dict() for product in products])

# GET produk detail by ID
@product_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    return jsonify(product.as_dict())

# POST produk baru
@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        description=data.get('description'),
        category_id=data['category_id'],
        user_id=data['user_id'],
        price=data['price'],
        unit_type=data.get('unit_type'),
        stock_quantity=data['stock_quantity'],
        organic=data.get('organic', False),
        discount_id=data.get('discount_id'),
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product created successfully'}), 201

# PUT update produk
@product_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    data = request.get_json()
    product.name = data['name']
    product.description = data.get('description', product.description)
    product.category_id = data['category_id']
    product.user_id = data['user_id']
    product.price = data['price']
    product.unit_type = data.get('unit_type', product.unit_type)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.organic = data.get('organic', product.organic)
    db.session.commit()
    return jsonify({'message': 'Product updated successfully'})

# DELETE produk
@product_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'})

# GET produk berdasarkan user_id (penjual tertentu)
@product_bp.route('/by-user/<int:user_id>', methods=['GET'])
def get_products_by_user(user_id):
    products = Product.query.filter_by(user_id=user_id).all()
    return jsonify([product.as_dict() for product in products])

# GET produk berdasarkan user_id
@product_bp.route('/seller/<int:user_id>', methods=['GET'])
def get_products_by_seller(user_id):
    products = Product.query.filter_by(user_id=user_id).all()
    return jsonify([p.as_dict() for p in products]), 200


# GET data singkat (ringkasan produk + penjualan)
@product_bp.route('/summary', methods=['GET'])
def get_product_summary():
    products = Product.query.all()
    result = []
    for product in products:
        total_sold = sum([item.quantity for item in product.order_items])  # butuh relasi ke OrderItem
        result.append({
            "product_id": product.product_id,
            "product_name": product.name,
            "sale": total_sold,
            "price": product.price,
            "stock": product.stock_quantity,
            "images": [img.image_url for img in product.images]
        })
    return jsonify(result), 200


