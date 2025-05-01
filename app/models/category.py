from app.extensions import db
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class Category(db.Model):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    image_url = Column(String)
    display_order = Column(Integer)

    products = relationship("Product", back_populates="category")

    
