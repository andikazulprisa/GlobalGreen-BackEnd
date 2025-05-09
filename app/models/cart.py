from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db
from app.models.cart_item import CartItem 

class Cart(db.Model):
    __tablename__ = 'carts'

    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    items = db.relationship('CartItem', backref='cart', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='cart', casecade='all, delete-orphan')

    def serialize(self):
        return {
            "items": [
                {
                    "product_id": item.product.product_id,
                    "name": item.product.name,
                    "image": item.product.images[0].image_url if item.product.images else None,
                    "price": item.product.price,
                    "category": item.product.category.name if item.product.category else None,
                    "unit_type": item.product.unit_type,
                    "quantity": item.quantity
                }
                for item in self.items
            ]
        }
