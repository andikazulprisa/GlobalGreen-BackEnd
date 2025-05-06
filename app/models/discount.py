from sqlalchemy import Column, Integer, String, Float, Boolean
from app.extensions import db

class Discount(db.Model):
    __tablename__ = "discounts"

    discount_id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True)
    description = Column(String)
    discount_type = Column(String, nullable=False)  # percentage or fixed
    discount_value = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)

    products = db.relationship("Product", back_populates="discounts")