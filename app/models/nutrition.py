from sqlalchemy import Column, Integer, Float, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.extensions import db

class Nutrition(db.Model):
    __tablename__ = "nutritions"

    nutrition_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    calories = Column(Float)
    protein = Column(Float)
    carbohydrates = Column(Float)
    fat = Column(Float)
    fiber = Column(Float)
    vitamins = Column(JSON)
    minerals = Column(JSON)
    serving_size = Column(String)

    product = relationship("Product", back_populates="nutrition")