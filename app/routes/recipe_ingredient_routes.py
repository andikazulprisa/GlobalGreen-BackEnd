from flask import Blueprint, request, jsonify
from app.models.recipe_ingredient import RecipeIngredient
from app.extensions import db

recipe_ingredient_bp = Blueprint('recipe_ingredient_bp', __name__)

@recipe_ingredient_bp.route('/', methods=['GET'])
def get_all_recipe_ingredients():
    ingredients = RecipeIngredient.query.all()
    return jsonify([i.as_dict() for i in ingredients])

@recipe_ingredient_bp.route('/<int:ingredient_id>', methods=['GET'])
def get_recipe_ingredient(ingredient_id):
    ingredient = RecipeIngredient.query.get_or_404(ingredient_id)
    return jsonify(ingredient.as_dict())

@recipe_ingredient_bp.route('/', methods=['POST'])
def create_recipe_ingredient():
    data = request.json
    ingredient = RecipeIngredient(**data)
    db.session.add(ingredient)
    db.session.commit()
    return jsonify(ingredient.as_dict()), 201

@recipe_ingredient_bp.route('/<int:ingredient_id>', methods=['PUT'])
def update_recipe_ingredient(ingredient_id):
    ingredient = RecipeIngredient.query.get_or_404(ingredient_id)
    data = request.json
    for key, value in data.items():
        setattr(ingredient, key, value)
    db.session.commit()
    return jsonify(ingredient.as_dict())

@recipe_ingredient_bp.route('/<int:ingredient_id>', methods=['DELETE'])
def delete_recipe_ingredient(ingredient_id):
    ingredient = RecipeIngredient.query.get_or_404(ingredient_id)
    db.session.delete(ingredient)
    db.session.commit()
    return jsonify({'message': 'Recipe ingredient deleted'})