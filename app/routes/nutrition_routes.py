from flask import Blueprint, request, jsonify
from app.models.nutrition import Nutrition
from app.extensions import db

nutrition_bp = Blueprint('nutrition_bp', __name__)

@nutrition_bp.route('/', methods=['GET'])
def get_nutritions():
    nutritions = Nutrition.query.all()
    return jsonify([n.as_dict() for n in nutritions])

@nutrition_bp.route('/<int:nutrition_id>', methods=['GET'])
def get_nutrition(nutrition_id):
    nutrition = Nutrition.query.get_or_404(nutrition_id)
    return jsonify(nutrition.as_dict())

@nutrition_bp.route('/', methods=['POST'])
def create_nutrition():
    data = request.json
    nutrition = Nutrition(**data)
    db.session.add(nutrition)
    db.session.commit()
    return jsonify(nutrition.as_dict()), 201

@nutrition_bp.route('/<int:nutrition_id>', methods=['PUT'])
def update_nutrition(nutrition_id):
    nutrition = Nutrition.query.get_or_404(nutrition_id)
    data = request.json
    for key, value in data.items():
        setattr(nutrition, key, value)
    db.session.commit()
    return jsonify(nutrition.as_dict())

@nutrition_bp.route('/<int:nutrition_id>', methods=['DELETE'])
def delete_nutrition(nutrition_id):
    nutrition = Nutrition.query.get_or_404(nutrition_id)
    db.session.delete(nutrition)
    db.session.commit()
    return jsonify({'message': 'Nutrition deleted'})

as_dict = lambda self: {
        "nutrition_id": self.nutrition_id,
        "product_id": self.product_id,
        "calories": self.calories,
        "protein": self.protein,
        "carbohydrates": self.carbohydrates,
        "fats": self.fats,
        "fiber": self.fiber,
        "vitamins": self.vitamins,
        "minerals": self.minerals,
        "serving_size": self.serving_size
    }