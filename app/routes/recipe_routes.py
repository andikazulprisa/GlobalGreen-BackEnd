from flask import Blueprint, request, jsonify
from app.models.recipe import Recipe
from app.extensions import db

recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/', methods=['GET'])
def get_all_recipes():
    recipes = Recipe.query.all()
    return jsonify([r.as_dict() for r in recipes])

@recipe_bp.route('/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.as_dict())

@recipe_bp.route('/', methods=['POST'])
def create_recipe():
    data = request.json
    recipe = Recipe(**data)
    db.session.add(recipe)
    db.session.commit()
    return jsonify(recipe.as_dict()), 201

@recipe_bp.route('/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    data = request.json
    for key, value in data.items():
        setattr(recipe, key, value)
    db.session.commit()
    return jsonify(recipe.as_dict())

@recipe_bp.route('/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({'message': 'Recipe deleted'})