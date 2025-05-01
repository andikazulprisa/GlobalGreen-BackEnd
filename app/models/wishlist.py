from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class Wishlist(db.Model):
    __tablename__ = "wishlists"

    wishlist_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    name = Column(String, nullable=False)

    user = relationship("User", back_populates="wishlists")
    items = relationship("WishlistItem", back_populates="wishlist")