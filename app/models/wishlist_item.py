from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class WishlistItem(db.Model):
    __tablename__ = "wishlist_items"

    wishlist_item_id = Column(Integer, primary_key=True, index=True)
    wishlist_id = Column(Integer, ForeignKey("wishlists.wishlist_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))

    wishlist = relationship("Wishlist", back_populates="items")
    product = relationship("Product")