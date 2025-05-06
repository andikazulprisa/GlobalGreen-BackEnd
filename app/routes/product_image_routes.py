from flask import Blueprint, request, jsonify
from app.models.product_image import ProductImage
from app.models.product import Product
from app.extensions import db

product_image_bp = Blueprint('product_image_bp', __name__)

# Get all product images
@product_image_bp.route('/', methods=['GET'])
def get_all_product_images():
    images = ProductImage.query.all()
    return jsonify([i.as_dict() for i in images])

# Get a single image by image_id
@product_image_bp.route('/<int:image_id>', methods=['GET'])
def get_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    return jsonify(image.as_dict())

# Get all images for a specific product
@product_image_bp.route('/product/<int:product_id>', methods=['GET'])
def get_images_by_product(product_id):
    images = ProductImage.query.filter_by(product_id=product_id).order_by(ProductImage.display_order).all()
    return jsonify([img.as_dict() for img in images])

# Add an image to a specific product
@product_image_bp.route('/product/<int:product_id>', methods=['POST'])
def add_image_to_product(product_id):
    data = request.get_json()

    if not data.get('image_url'):
        return jsonify({"error": "image_url is required"}), 400

    # Optional: check if product exists
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    image = ProductImage(
        product_id=product_id,
        image_url=data['image_url'],
        alt_text=data.get('alt_text'),
        display_order=data.get('display_order', 0)
    )
    db.session.add(image)
    db.session.commit()
    return jsonify(image.as_dict()), 201

# Update a product image
@product_image_bp.route('/<int:image_id>', methods=['PUT'])
def update_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    data = request.get_json()

    for key in ['image_url', 'alt_text', 'display_order']:
        if key in data:
            setattr(image, key, data[key])

    db.session.commit()
    return jsonify(image.as_dict())

# Delete a product image
@product_image_bp.route('/<int:image_id>', methods=['DELETE'])
def delete_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'message': 'Product image deleted successfully'})
