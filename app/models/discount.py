from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime
from app.extensions import db

class Discount(db.Model):
    __tablename__ = "discounts"

    discount_id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, unique=True)
    description = Column(String)
    discount_type = Column(String, nullable=False)  # "percentage" or "fixed"
    discount_value = Column(Float, nullable=False)
    valid_from = Column(DateTime, default=datetime.utcnow)
    valid_to = Column(DateTime)
    is_active = Column(Boolean, default=True)

    products = db.relationship("Product", back_populates="discount")

    def to_dict(self):
        return {
            "discount_id": self.discount_id,
            "code": self.code,
            "description": self.description,
            "discount_type": self.discount_type,
            "discount_value": self.discount_value,
            "valid_from": self.valid_from.isoformat() if self.valid_from else None,
            "valid_to": self.valid_to.isoformat() if self.valid_to else None,
            "is_active": self.is_active
        }
