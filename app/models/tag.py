from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.extensions import db

class Tag(db.Model):
    __tablename__ = "tags"

    tag_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    recipes = relationship("RecipeTag", back_populates="tag")