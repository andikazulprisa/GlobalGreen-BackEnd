from flask import Blueprint, request, jsonify
from app.models.review import Review
from app.extensions import db

review_bp = Blueprint('review_bp', __name__)

@review_bp.route('/', methods=['GET'])
def get_all_reviews():
    reviews = Review.query.all()
    return jsonify([r.as_dict() for r in reviews])

@review_bp.route('/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.get_or_404(review_id)
    return jsonify(review.as_dict())

@review_bp.route('/', methods=['POST'])
def create_review():
    data = request.json
    review = Review(**data)
    db.session.add(review)
    db.session.commit()
    return jsonify(review.as_dict()), 201

@review_bp.route('/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.json
    for key, value in data.items():
        setattr(review, key, value)
    db.session.commit()
    return jsonify(review.as_dict())

@review_bp.route('/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted'})