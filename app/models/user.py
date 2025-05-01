from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    role = Column(Enum("Customer", "Admin", "Staff", name="user_roles"), default="Customer")

    # Relationships
    addresses = relationship("Address", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    cart = db.relationship('Cart', back_populates='user', uselist=False)
    wishlists = relationship("Wishlist", back_populates="user")

    # Menambahkan metode as_dict di sini
    def as_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'created_at': self.created_at,
            'role': self.role
        }
