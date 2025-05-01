from sqlalchemy import Column, Integer, ForeignKey
from app.extensions import db

class ShoppingCart(db.Model):
    __tablename__ = "shopping_carts"
    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
