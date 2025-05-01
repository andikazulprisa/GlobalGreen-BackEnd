from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.extensions import db

class Recipe(db.Model):
    __tablename__ = "recipes"

    recipe_id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    instructions = Column(Text)
    image_url = Column(String)
    author = Column(String)

    ingredients = relationship("RecipeIngredient", back_populates="recipe")
    tags = relationship("RecipeTag", back_populates="recipe")