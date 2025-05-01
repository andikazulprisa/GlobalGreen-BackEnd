from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class CartItem(db.Model):
    __tablename__ = 'cart_items'

    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.cart_id'), nullable=False)
    product = db.relationship('Product', back_populates='cart_items')
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)

    cart = db.relationship('Cart', back_populates='items')