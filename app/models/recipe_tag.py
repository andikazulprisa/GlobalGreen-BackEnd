from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class RecipeTag(db.Model):
    __tablename__ = "recipe_tags"

    recipe_tag_id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.recipe_id"))
    tag_id = Column(Integer, ForeignKey("tags.tag_id"))

    recipe = relationship("Recipe", back_populates="tags")
    tag = relationship("Tag", back_populates="recipes")