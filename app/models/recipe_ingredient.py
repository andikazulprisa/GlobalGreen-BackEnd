from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class RecipeIngredient(db.Model):
    __tablename__ = "recipe_ingredients"

    recipe_ingredient_id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    ingredient_name = Column(String)
    quantity = Column(Integer)
    unit = Column(String)

    recipe = relationship("Recipe", back_populates="ingredients")
    product = relationship("Product")