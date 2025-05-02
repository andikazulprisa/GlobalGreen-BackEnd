from flask import Blueprint, request, jsonify
from app.models.recipe_tag import RecipeTag
from app.extensions import db

recipe_tag_bp = Blueprint('recipe_tag_bp', __name__)

@recipe_tag_bp.route('/', methods=['GET'])
def get_all_recipe_tags():
    tags = RecipeTag.query.all()
    return jsonify([t.as_dict() for t in tags])

@recipe_tag_bp.route('/<int:recipe_tag_id>', methods=['GET'])
def get_recipe_tag(recipe_tag_id):
    tag = RecipeTag.query.get_or_404(recipe_tag_id)
    return jsonify(tag.as_dict())

@recipe_tag_bp.route('/', methods=['POST'])
def create_recipe_tag():
    data = request.json
    tag = RecipeTag(**data)
    db.session.add(tag)
    db.session.commit()
    return jsonify(tag.as_dict()), 201

@recipe_tag_bp.route('/<int:recipe_tag_id>', methods=['PUT'])
def update_recipe_tag(recipe_tag_id):
    tag = RecipeTag.query.get_or_404(recipe_tag_id)
    data = request.json
    for key, value in data.items():
        setattr(tag, key, value)
    db.session.commit()
    return jsonify(tag.as_dict())

@recipe_tag_bp.route('/<int:recipe_tag_id>', methods=['DELETE'])
def delete_recipe_tag(recipe_tag_id):
    tag = RecipeTag.query.get_or_404(recipe_tag_id)
    db.session.delete(tag)
    db.session.commit()
    return jsonify({'message': 'Recipe tag deleted'})