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
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)  # Produk milik seller
    price = Column(Float, nullable=False)
    unit_type = Column(String)
    stock_quantity = Column(Integer)
    organic = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relationships
    category = relationship("Category", back_populates="products")
    category_id = Column(Integer, ForeignKey("categories.category_id"))
    user = relationship("User", back_populates="products")
    images = relationship("ProductImage", back_populates="product", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="product")
    cart_items = relationship('CartItem', back_populates='product', cascade='all, delete-orphan')
    wishlist_items = relationship("WishlistItem", back_populates="product")
    nutrition = relationship("Nutrition", back_populates="product", uselist=False)
    order_items = relationship("OrderItem", back_populates="product")
    recipe_ingredients = relationship("RecipeIngredient", back_populates="product")
    discount_id = Column(Integer, ForeignKey("discounts.discount_id"), nullable=True)
    discount = relationship("Discount", back_populates="products")

    def as_dict(self):
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "category_id": self.category_id,
            "user_id": self.user_id,
            "price": self.price,
            "unit_type": self.unit_type,
            "stock_quantity": self.stock_quantity,
            "organic": self.organic,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "update_at": self.update_at.isoformat() if self.update_at else None,
            "images": [image.as_dict() for image in self.images],
            "nutrition": self.nutrition.as_dict() if self.nutrition else None,
            "discount": {
                "code": self.discount.code,
                "type": self.discount.discount_type,
                "value": self.discount.discount_value,
                "is_active": self.discount.is_active
            } if self.discount else None
        }
