from flask import Blueprint, request, jsonify
from app.models.tag import Tag
from app.extensions import db

tag_bp = Blueprint('tag_bp', __name__)

@tag_bp.route('/', methods=['GET'])
def get_all_tags():
    tags = Tag.query.all()
    return jsonify([t.as_dict() for t in tags])

@tag_bp.route('/<int:tag_id>', methods=['GET'])
def get_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return jsonify(tag.as_dict())

@tag_bp.route('/', methods=['POST'])
def create_tag():
    data = request.json
    tag = Tag(**data)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.as_dict()), 201

@tag_bp.route('/<int:tag_id>', methods=['PUT'])
def update_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    data = request.json
    for key, value in data.items():
        setattr(tag, key, value)
    db.session.commit()
    return jsonify(tag.as_dict())

@tag_bp.route('/<int:tag_id>', methods=['DELETE'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Tag deleted'})