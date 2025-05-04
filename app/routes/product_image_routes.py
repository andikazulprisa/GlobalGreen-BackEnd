from flask import Blueprint, request, jsonify
from app.models.product_image import ProductImage
from app.extensions import db

product_image_bp = Blueprint('product_image_bp', __name__)

@product_image_bp.route('/', methods=['GET'])
def get_all_product_images():
    images = ProductImage.query.all()
    return jsonify([i.as_dict() for i in images])

@product_image_bp.route('/<int:image_id>', methods=['GET'])
def get_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    return jsonify(image.as_dict())

@product_image_bp.route('/', methods=['POST'])
def create_product_image():
    data = request.json
    image = ProductImage(**data)
    db.session.add(image)
    db.session.commit()
    return jsonify(image.as_dict()), 201

@product_image_bp.route('/product/<int:product_id>', methods=['POST'])
def add_image_to_product(product_id):
    data = request.get_json()
    image = ProductImage(
        product_id=product_id,
        image_url=data['image_url'],
        alt_text=data.get('alt_text'),
        display_order=data.get('display_order', 0)
    )
    db.session.add(image)
    db.session.commit()
    return jsonify(image.as_dict()), 201

@product_image_bp.route('/<int:image_id>', methods=['PUT'])
def update_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    data = request.json
    for key, value in data.items():
        setattr(image, key, value)
    db.session.commit()
    return jsonify(image.as_dict())

@product_image_bp.route('/<int:image_id>', methods=['DELETE'])
def delete_product_image(image_id):
    image = ProductImage.query.get_or_404(image_id)
    db.session.delete(image)
    db.session.commit()
    return jsonify({'message': 'Product image deleted'})