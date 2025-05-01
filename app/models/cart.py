from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class Cart(db.Model):
    __tablename__ = 'carts'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    user = db.relationship('User', back_populates='cart')  # ✅ tambahkan ini
    items = db.relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
