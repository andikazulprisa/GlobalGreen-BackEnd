from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..extensions import db


class Product(db.Model):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    price = Column(Float, nullable=False)
    unit_type = Column(String)
    stock_quantity = Column(Integer)
    image_url = Column(String)
    organic = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")
    images = relationship("ProductImage", back_populates="product")
    reviews = relationship("Review", back_populates="product")
    cart_items = db.relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
    wishlist_items = relationship("WishlistItem", back_populates="product")
    nutrition = relationship("Nutrition", back_populates="product", uselist=False)
    recipe_ingredients = relationship("RecipeIngredient", back_populates="product")

    def as_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "price": self.price,
            "unit_type": self.unit_type,
            "stock_quantity": self.stock_quantity,
            "image_url": self.image_url,
            "organic": self.organic,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "update_at": self.update_at.isoformat() if self.update_at else None
        }