from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class Review(db.Model):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))
    rating = Column(Integer)
    review_text = Column(String)
    review_date = Column(DateTime, default=datetime.now)
    is_verified_purchase = Column(Boolean)

    product = relationship("Product", back_populates="reviews")
    user = relationship("User", back_populates="reviews")