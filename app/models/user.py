from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from sqlalchemy import Enum as PgEnum

# Enum untuk role user
class UserRole(enum.Enum):
    Customer = "Customer"
    Seller = "Seller"

class User(db.Model):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    _password = Column("password", String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    phone = Column(String)
    image_url = Column(String) 
    created_at = Column(DateTime, default=datetime.now)
    # Menggunakan PgEnum untuk enum role
    role = Column(PgEnum(UserRole, name="user_roles", create_constraint=True, native_enum=False), default=UserRole.Customer)

    # Relationships
    addresses = relationship("Address", back_populates="user")
    products = relationship("Product", back_populates="user")
    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")
    cart = db.relationship('Cart', back_populates='user', uselist=False)
    wishlists = relationship("Wishlist", back_populates="user")

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, plain_password):
        self._password = generate_password_hash(plain_password)

    def check_password(self, plain_password):
        return check_password_hash(self._password, plain_password)

    def as_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'image_url': self.image_url,
            'created_at': self.created_at,
            'role': self.role.value
        }
